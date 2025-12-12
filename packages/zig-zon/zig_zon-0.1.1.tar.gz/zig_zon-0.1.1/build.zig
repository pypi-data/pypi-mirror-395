const std = @import("std");
const Build = std.Build;

const CPython = @import("setuptools_zig_build").CPython;

pub fn build(b: *Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});
    const python = CPython.findAddOption(b);
    python.addVersionOption(b, @import("build.zig.zon").version);

    CPython.addSdistList(b);

    const lib = b.addLibrary(.{
        .name = "zig_zon",
        .root_module = b.addModule("zig_zon", .{
            .root_source_file = b.path("src/zig_zon.zig"),
            .target = target,
            .optimize = optimize,
        }),
        .linkage = .dynamic,
        .use_llvm = true,
    });
    CPython.installExtLib(b, lib);

    python.link(b, .{
        .lib = lib,
    });

    const install_test = b.addInstallFile(b.path("src/test_zig_zon.py"), "lib/test_zig_zon.py");
    b.step("install-test", "install the python test script alongside the built modules").dependOn(&install_test.step);

    const run_test = python.run_test(b, lib, b.path("src/test_zig_zon.py"));

    b.step("test", "run the python test script").dependOn(&run_test.step);
}
