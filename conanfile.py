from conans import ConanFile, tools


class GlogConan(ConanFile):
    # name = "TODO_NAME"
    # version = "TODO_VERSION"
    author = "None"

    description = "<Description of Glog here>"
    license = "MIT"
    topics = None
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    exports_sources = "package/*"

    def package(self):
        self.copy("*", src="package")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
