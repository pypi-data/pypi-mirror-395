const std = @import("std");

pub fn main() !void {
    var gpa_impl = std.heap.DebugAllocator(.{}).init;
    defer _ = gpa_impl.deinit();
    const gpa = gpa_impl.allocator();

    const args = try std.process.argsAlloc(gpa);
    defer std.process.argsFree(gpa, args);

    if (args.len != 4) {
        std.log.err("expected n args, got: {d}", .{args.len});
        return error.Expected4Arguments;
    }

    const python = args[1];
    const pythonpath = args[2];
    const test_file = args[3];

    const pythonpath_abs = if (std.fs.path.isAbsolute(pythonpath)) try gpa.dupe(u8, pythonpath) else blk: {
        const cwd = try std.process.getCwdAlloc(gpa);
        defer gpa.free(cwd);
        break :blk try std.fs.path.join(gpa, &.{ cwd, pythonpath });
    };
    defer gpa.free(pythonpath_abs);

    std.log.info("PYTHONPATH={s} {s} {s}", .{
        pythonpath_abs,
        python,
        test_file,
    });

    const argv: []const []const u8 = &.{
        python,
        test_file,
    };

    var env = try std.process.getEnvMap(gpa);
    defer env.deinit();
    try env.put("PYTHONPATH", pythonpath_abs);

    var proc: std.process.Child = .init(argv, gpa);
    proc.env_map = &env;
    proc.stderr_behavior = .Inherit;
    proc.stdin_behavior = .Inherit;
    proc.stdout_behavior = .Inherit;
    const res = try proc.spawnAndWait();
    std.process.exit(res.Exited);
}
