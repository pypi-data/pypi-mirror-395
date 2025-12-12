const std = @import("std");
const Ast = std.zig.Ast;
const Allocator = std.mem.Allocator;
const assert = std.debug.assert;
const ZonGen = std.zig.ZonGen;

const python = @import("cpython");
const c = python.c;
const PyObject = c.PyObject;

const PyModuleDef_Base = extern struct {
    ob_base: PyObject,
    // m_init: ?fn () callconv(.C) [*c]PyObject = null,
    m_init: ?*const fn () callconv(.c) [*c]PyObject = null,
    m_index: c.Py_ssize_t = 0,
    m_copy: [*c]PyObject = null,
};

pub var methods = [_]c.PyMethodDef{
    c.PyMethodDef{
        .ml_name = "parse",
        .ml_meth = @ptrCast(@alignCast(&parse)),
        .ml_flags = @as(c_int, 1),
        .ml_doc = "parse a zon literal to a python object",
    },
    c.PyMethodDef{},
};

pub var zigmodule = c.PyModuleDef{
    .m_name = "zig_zon",
    .m_methods = &methods,
};

pub export fn PyInit_zig_zon() [*c]c.PyObject {
    const mod = c.PyModule_Create(&zigmodule);
    const semver = std.SemanticVersion.parse(python.version) catch unreachable;
    const version = c.PyDict_New();

    _ = c.PyDict_SetItemString(version, "major", c.Py_BuildValue("n", semver.major));
    _ = c.PyDict_SetItemString(version, "minor", c.Py_BuildValue("n", semver.minor));
    _ = c.PyDict_SetItemString(version, "patch", c.Py_BuildValue("n", semver.patch));
    if (semver.pre) |pre| {
        _ = c.PyDict_SetItemString(version, "pre", c.Py_BuildValue("s#", pre.ptr, pre.len));
    } else {
        _ = c.PyDict_SetItemString(version, "pre", PyNone());
    }
    if (semver.build) |build| {
        _ = c.PyDict_SetItemString(version, "build", c.Py_BuildValue("s#", build.ptr, build.len));
    } else {
        _ = c.PyDict_SetItemString(version, "build", PyNone());
    }
    _ = c.PyObject_SetAttrString(
        mod,
        "__version__",
        version,
    );

    const version_str = c.Py_BuildValue("s#", python.version.ptr, python.version.len);
    _ = c.PyObject_SetAttrString(
        mod,
        "__version_str__",
        version_str,
    );
    return mod;
}

pub fn parse(self: [*]PyObject, args: [*]PyObject) callconv(.c) [*c]PyObject {
    _ = self;
    var zon_txt: [*c]u8 = undefined;
    if (!(c.PyArg_ParseTuple(args, "s", &zon_txt) != 0)) return null;

    var arena_instance = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_instance.deinit();
    const arena = arena_instance.allocator();

    const ast = Ast.parse(arena, std.mem.sliceTo(zon_txt, 0), .zon) catch |err| {
        const errstr = std.fmt.allocPrintSentinel(
            arena,
            "zig-zon ast error: {s}",
            .{@errorName(err)},
            0,
        ) catch "";
        c.PyErr_SetString(c.PyExc_Exception, errstr.ptr);
        return null;
    };

    // TODO: use zoir instead of AST maybe?
    // this is unused for now and instead i walk the AST, but i keep it in as a sanity check for now.
    var zoir = ZonGen.generate(arena, ast, .{ .parse_str_lits = false }) catch |err| {
        const errstr = std.fmt.allocPrintSentinel(
            arena,
            "zig-zon zoir error: {s}",
            .{@errorName(err)},
            0,
        ) catch "";
        c.PyErr_SetString(c.PyExc_Exception, errstr.ptr);
        return null;
    };
    defer zoir.deinit(arena);

    const main_node_index = ast.nodeData(.root).node;

    return parseZon(arena, ast, main_node_index) catch |err| {
        const errstr = std.fmt.allocPrintSentinel(
            arena,
            "zig-zon parse error: {s}",
            .{@errorName(err)},
            0,
        ) catch "";
        c.PyErr_SetString(c.PyExc_Exception, errstr.ptr);
        return null;
    };
}

inline fn PyNone() [*c]c.PyObject {
    return c.Py_BuildValue("");
}

const ZonError = error{
    StructExpected,
    StructIdentifierExpected,
    NotImplemented,
    ZonArrayError,
} || IdentifierError || NumberLiteralError;

fn parseZon(arena: Allocator, tree: Ast, node: Ast.Node.Index) ZonError!*c.PyObject {
    const node_tag = tree.nodeTag(node);
    switch (node_tag) {
        .struct_init_comma,
        .struct_init_dot_comma,
        .struct_init_dot_two_comma,
        .struct_init_dot_two,
        .struct_init_dot,
        .struct_init_one_comma,
        .struct_init_one,
        .struct_init,
        => return parseZonStruct(arena, tree, node),
        .array_init_comma,
        .array_init_dot_comma,
        .array_init_dot_two_comma,
        .array_init_dot_two,
        .array_init_dot,
        .array_init_one_comma,
        .array_init_one,
        .array_init,
        => return parseZonArray(arena, tree, node),
        .enum_literal => {
            const name_token = tree.firstToken(node);
            const enum_name = tree.tokenSlice(name_token + 1);
            if (std.mem.startsWith(u8, enum_name, "@")) {
                std.log.err("non bare enum literals not implemented: {s}", .{enum_name});
                return error.NotImplemented;
            }

            return c.Py_BuildValue("s#", enum_name.ptr, enum_name.len);
        },
        .string_literal => {
            const name_token = tree.firstToken(node);
            const name = tree.tokenSlice(name_token);
            var buf = std.ArrayListUnmanaged(u8).empty;
            try parseStrLit(arena, &buf, name, 0);
            return c.Py_BuildValue("s#", buf.items.ptr, buf.items.len);
        },
        .negation => return parseNumberLiteral(arena, tree, node, true),
        .number_literal => return parseNumberLiteral(arena, tree, node, false),
        .identifier => {
            const token_slice = tree.tokenSlice(tree.firstToken(node));
            if (std.mem.eql(u8, token_slice, "true")) {
                return c.PyBool_FromLong(@as(c_long, 1));
            } else if (std.mem.eql(u8, token_slice, "false")) {
                return c.PyBool_FromLong(@as(c_long, 0));
            } else if (std.mem.eql(u8, token_slice, "null")) {
                return PyNone();
            } else {
                if (@errorReturnTrace()) |et| {
                    std.debug.dumpStackTrace(et.*);
                    std.debug.dumpCurrentStackTrace(null);
                }
                std.log.err("identifier not implemented: {any} '{s}'", .{ node_tag, token_slice });
                return error.NotImplemented;
            }
        },
        else => {
            if (@errorReturnTrace()) |et| {
                std.debug.dumpStackTrace(et.*);
                std.debug.dumpCurrentStackTrace(null);
            }
            const token_slice = tree.tokenSlice(tree.firstToken(node));
            std.log.err("zon ast token not implemented: {any} '{s}'", .{ node_tag, token_slice });
            return error.NotImplemented;
        },
    }
}

const NumberLiteralError = error{
    BigIntNotImplemented,
    InvalidCharacter,
    HexFloatNotImplemented,
    NumberLiteralFail,
};

fn parseNumberLiteral(arena: Allocator, tree: Ast, node: Ast.Node.Index, negated: bool) NumberLiteralError!*c.PyObject {
    _ = arena;
    const num_token = tree.lastToken(node);
    const token_bytes = tree.tokenSlice(num_token);
    const parsed = std.zig.parseNumberLiteral(token_bytes);
    switch (parsed) {
        .int => |n| {
            const factor: i64 = if (negated) -1 else 1;
            const neglim = 9223372036854775807; // 2**63 - 1
            if (n <= neglim) {
                return c.PyLong_FromSsize_t(factor * @as(i64, @intCast(n)));
            } else {
                if (factor == -1) return error.BigIntNotImplemented;
                return c.PyLong_FromSize_t(n);
            }
        },
        .big_int => return error.BigIntNotImplemented,
        .float => |n| {
            const float_payload = switch (n) {
                .decimal => token_bytes,
                .hex => return error.HexFloatNotImplemented,
            };
            const float = try std.fmt.parseFloat(f64, float_payload);
            const factor: f64 = if (negated) -1 else 1;

            return c.Py_BuildValue("f", factor * float);
        },
        .failure => |err| {
            std.log.err("number literal: {} bytes: {s}", .{ err, token_bytes });
            return error.NumberLiteralFail;
        },
    }
}

fn parseZonStruct(arena: Allocator, tree: Ast, node: Ast.Node.Index) ZonError!*c.PyObject {
    var buf: [2]Ast.Node.Index = undefined;
    const struct_init = tree.fullStructInit(&buf, node) orelse return error.StructExpected;

    const ret = c.PyDict_New();

    for (struct_init.ast.fields) |field_init| {
        const name_token = tree.firstToken(field_init) - 2;
        const field_name = try identifierTokenString(arena, tree, name_token);
        const field_obj = try parseZon(arena, tree, field_init);
        const set_result = c.PyDict_SetItemString(ret, field_name, field_obj);
        assert(set_result >= 0);
    }
    return ret;
}

fn parseZonArray(arena: Allocator, tree: Ast, node: Ast.Node.Index) !*c.PyObject {
    // ret.* = c.Py_BuildValue("l", @as(u64, 1));
    var buf: [2]Ast.Node.Index = undefined;
    const array_init = tree.fullArrayInit(&buf, node) orelse {
        const tok = tree.nodeMainToken(node);
        std.log.err("expected paths expression to be a list of strings, got: {d}", .{tok});
        return error.ZonArrayError;
    };

    const ret = c.PyList_New(0);

    for (array_init.ast.elements) |elem_node| {
        const field_ret = try parseZon(arena, tree, elem_node);
        assert(c.PyList_Append(ret, field_ret) >= 0);
    }
    return ret;
}

const IdentifierError = error{OutOfMemory} || StringLiteralError;

fn identifierTokenString(arena: Allocator, ast: Ast, token: Ast.TokenIndex) IdentifierError![:0]const u8 {
    std.debug.assert(ast.tokenTag(token) == .identifier);
    const ident_name = ast.tokenSlice(token);
    if (!std.mem.startsWith(u8, ident_name, "@")) {
        return try arena.dupeZ(u8, ident_name);
    }

    var buf = std.ArrayListUnmanaged(u8).empty;
    try parseStrLit(arena, &buf, ident_name, 1);
    try buf.append(arena, 0);
    return @ptrCast(buf.items);
}

const StringLiteralError = error{
    StringLiteralFail,
    WriteFailed,
};

fn parseStrLit(
    arena: Allocator,
    buf: *std.ArrayListUnmanaged(u8),
    bytes: []const u8,
    offset: u32,
) StringLiteralError!void {
    const raw_string = bytes[offset..];
    const result = r: {
        var aw: std.Io.Writer.Allocating = .fromArrayList(arena, buf);
        defer buf.* = aw.toArrayList();
        break :r try std.zig.string_literal.parseWrite(&aw.writer, raw_string);
    };
    switch (result) {
        .success => {},
        .failure => |err| {
            std.log.err("StringLiteralFail: {}", .{err});
            return error.StringLiteralFail;
        },
    }
}
