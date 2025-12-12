const std = @import("std");
const builtin = @import("builtin");
const Build = std.Build;
const fs = std.fs;
const mem = std.mem;

pub const CPython = @This();

exe: Build.LazyPath,
version: ?[]const u8 = null,

/// adds a `python` option to the build. if not provided, tries to find `python` in PATH
pub fn findAddOption(b: *Build) *CPython {
    if (b.option(
        Build.LazyPath,
        "python",
        "path to the cpython interpreter executable",
    )) |opt| {
        const self = b.allocator.create(CPython) catch @panic("OOM");
        self.* = .{
            .exe = opt,
        };
        return self;
    } else return find(b);
}

pub fn find(b: *Build) *CPython {
    const self = b.allocator.create(CPython) catch @panic("OOM");
    const exe_path = FindExeWindowsCompat.findProgram(b, &.{
        "python",
        "python3",
    }, &.{}) catch {
        const err_wf = b.addWriteFiles();
        const err_step = b.addFail("finding python failed. please provide a path to the exe using -Dpython=");
        err_wf.step.dependOn(&err_step.step);
        self.* = .{ .exe = err_wf.getDirectory() };
        return self;
    };
    self.* = .{
        .exe = .{
            .cwd_relative = exe_path,
        },
    };
    return self;
}

pub fn addVersionOption(self: *CPython, b: *Build, fallback: []const u8) void {
    self.version = b.option(
        []const u8,
        "version",
        "set a version string",
    ) orelse fallback;
}

pub const LinkOptions = struct {
    /// library to link against libpython
    lib: *std.Build.Step.Compile,
    macros: []const [2][]const u8 = &default_macros,
    pub const default_macros = .{
        .{ "Py_LIMITED_API", "0x03060500" }, // use the limited api from 3.6.5
    };
};

pub fn generateIncludeDir(self: CPython, b: *Build) Build.LazyPath {
    const extract_link_info = Build.Step.Run.create(b, "python header extraction run");
    extract_link_info.addFileArg(self.exe);
    const wf = b.addWriteFiles();
    extract_link_info.addFileArg(wf.add("extract_link_info.py", @embedFile("extract_link_info.py")));
    return extract_link_info.addOutputDirectoryArg("include");
}

pub fn installExtLib(b: *Build, lib: *Build.Step.Compile) void {
    const ext_lib_name = lib_ext_name(b, lib);
    const lib_install = b.addInstallLibFile(lib.getEmittedBin(), ext_lib_name);
    b.getInstallStep().dependOn(&lib_install.step);
}

pub fn link(self: CPython, b: *Build, opt: LinkOptions) void {
    const target = Build.ResolvedTarget{
        .query = .{},
        .result = opt.lib.rootModuleTarget(),
    };

    const python_inc = self.generateIncludeDir(b);

    const cpython = b.addTranslateC(.{
        .root_source_file = python_inc.path(b, "Zig_Python_With_Hexver.h"),
        .optimize = opt.lib.root_module.optimize orelse .ReleaseSafe,
        .target = target,
        .link_libc = true,
    });
    cpython.addIncludePath(python_inc);

    const wf = b.addWriteFiles();
    const pymod_lp = wf.add("python.zig", if (self.version == null)
        \\pub const c = @import("c");
        \\
    else
        \\pub const c = @import("c");
        \\pub const version = @embedFile("version.txt");
        \\
    );
    if (self.version) |version| {
        _ = wf.add("version.txt", version);
    }

    const pymod = b.createModule(.{ .root_source_file = pymod_lp });
    pymod.addImport("c", cpython.createModule());

    for (opt.macros) |macro| {
        cpython.defineCMacro(macro[0], macro[1]);
    }

    if (target.result.os.tag == .windows) {
        opt.lib.root_module.addLibraryPath(python_inc);
        opt.lib.linkSystemLibrary("python");
    }
    opt.lib.root_module.addImport(
        "cpython",
        pymod,
    );
}

pub fn lib_ext_name(b: *Build, lib: *Build.Step.Compile) []const u8 {
    const target = lib.rootModuleTarget();
    return if (target.os.tag == .windows)
        b.fmt("{s}.pyd", .{lib.name})
    else
        b.fmt("{s}.so", .{lib.name});
}

pub fn run_test(
    self: CPython,
    b: *Build,
    lib: *Build.Step.Compile,
    test_py_file: Build.LazyPath,
) *Build.Step.Run {
    const wf = b.addWriteFiles();
    const python_runner = wf.add("python-runner.zig", @embedFile("python-runner.zig"));

    const runner = b.addExecutable(.{
        .name = "python-runner",
        .root_module = b.createModule(.{
            .root_source_file = python_runner,
            .target = b.graph.host,
            .optimize = .ReleaseSmall,
        }),
    });
    const run_step = b.addRunArtifact(runner);
    const python_ext = writeExtensionFile(b, lib);
    run_step.addFileArg(self.exe);
    run_step.addDirectoryArg(python_ext.dirname());
    run_step.addFileArg(test_py_file);
    run_step.has_side_effects = true;
    return run_step;
}

pub fn writeExtensionFile(b: *Build, lib: *Build.Step.Compile) Build.LazyPath {
    const ext_lib_name = lib_ext_name(b, lib);
    const wf = b.addWriteFiles();
    return wf.addCopyFile(lib.getEmittedBin(), ext_lib_name);
}

const FindExeWindowsCompat = struct {
    fn tryFindProgram(b: *Build, full_path: []const u8) ?[]const u8 {
        if (fs.realpathAlloc(b.allocator, full_path)) |p| {
            return p;
        } else |err| switch (err) {
            error.OutOfMemory => @panic("OOM"),
            else => {},
        }

        if (builtin.os.tag == .windows) {
            if (b.graph.env_map.get("PATHEXT")) |PATHEXT| {
                var it = mem.tokenizeScalar(u8, PATHEXT, fs.path.delimiter);

                while (it.next()) |ext| {
                    if (!supportedWindowsProgramExtension(ext)) continue;
                    const exe_path = mem.join(b.allocator, "", &.{ full_path, ext }) catch @panic("OOM");
                    fs.accessAbsolute(exe_path, .{ .mode = .read_only }) catch {
                        b.allocator.free(exe_path);
                        continue;
                    };
                    return exe_path;
                }
            }
        }

        return null;
    }

    pub fn findProgram(b: *Build, names: []const []const u8, paths: []const []const u8) error{FileNotFound}![]const u8 {
        // TODO report error for ambiguous situations
        for (b.search_prefixes.items) |search_prefix| {
            for (names) |name| {
                if (fs.path.isAbsolute(name)) {
                    return name;
                }
                return tryFindProgram(b, b.pathJoin(&.{ search_prefix, "bin", name })) orelse continue;
            }
        }
        if (b.graph.env_map.get("PATH")) |PATH| {
            for (names) |name| {
                if (fs.path.isAbsolute(name)) {
                    return name;
                }
                var it = mem.tokenizeScalar(u8, PATH, fs.path.delimiter);
                while (it.next()) |p| {
                    return tryFindProgram(b, b.pathJoin(&.{ p, name })) orelse continue;
                }
            }
        }
        for (names) |name| {
            if (fs.path.isAbsolute(name)) {
                return name;
            }
            for (paths) |p| {
                return tryFindProgram(b, b.pathJoin(&.{ p, name })) orelse continue;
            }
        }
        return error.FileNotFound;
    }

    fn supportedWindowsProgramExtension(ext: []const u8) bool {
        inline for (@typeInfo(std.process.Child.WindowsExtension).@"enum".fields) |field| {
            if (std.ascii.eqlIgnoreCase(ext, "." ++ field.name)) return true;
        }
        return false;
    }
};

pub fn addSdistList(b: *Build) void {
    const wf = b.addWriteFiles();
    var wr: std.Io.Writer.Allocating = .init(b.allocator);
    var jw: std.json.Stringify = .{ .writer = &wr.writer };
    jw.beginObject() catch @panic("OOM");
    if (b.graph.global_cache_root.path) |global_cache| {
        jw.objectField("global_cache_dir") catch @panic("OOM");
        jw.write(global_cache) catch @panic("OOM");
    }

    jw.objectField("dependencies") catch @panic("OOM");
    jw.beginArray() catch @panic("OOM");
    writeDeps(b, &jw) catch @panic("OOM");
    jw.endArray() catch @panic("OOM");
    jw.endObject() catch @panic("OOM");

    const out = wf.add("sdistlist.json", wr.written());
    const sdist_step = b.step("sdistlist", "generate a list of files for python sdist");
    sdist_step.dependOn(&b.addInstallFile(out, "sdistlist.json").step);
}

fn writeDeps(b: *std.Build, w: *std.json.Stringify) !void {
    for (b.available_deps) |dep| {
        try w.beginArray();
        try w.write(dep[0]);
        try w.write(dep[1]);
        try w.endArray();
        if (b.lazyDependency(dep[0], .{})) |lazy_dep| {
            try writeDeps(lazy_dep.builder, w);
        }
    }
}
