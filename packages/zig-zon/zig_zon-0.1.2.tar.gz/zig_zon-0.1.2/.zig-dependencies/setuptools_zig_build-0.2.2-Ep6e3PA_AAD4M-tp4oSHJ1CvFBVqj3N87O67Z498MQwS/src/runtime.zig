const std = @import("std");

pub fn addVersion(python: type, mod: [*c]python.c.PyObject) void {
    const c = python.c;
    const semver = std.SemanticVersion.parse(python.version) catch unreachable;
    const version = c.PyDict_New();

    _ = c.PyDict_SetItemString(version, "major", c.Py_BuildValue("n", semver.major));
    _ = c.PyDict_SetItemString(version, "minor", c.Py_BuildValue("n", semver.minor));
    _ = c.PyDict_SetItemString(version, "patch", c.Py_BuildValue("n", semver.patch));
    if (semver.pre) |pre| {
        _ = c.PyDict_SetItemString(version, "pre", c.Py_BuildValue("s#", pre.ptr, pre.len));
    } else {
        _ = c.PyDict_SetItemString(version, "pre", c.Py_BuildValue(""));
    }
    if (semver.build) |build| {
        _ = c.PyDict_SetItemString(version, "build", c.Py_BuildValue("s#", build.ptr, build.len));
    } else {
        _ = c.PyDict_SetItemString(version, "build", c.Py_BuildValue(""));
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
}
