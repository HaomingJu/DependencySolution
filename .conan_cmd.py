import os
import sys
import ConfigParser

def ReadProperty(file_path):
    ProSet = {}
    with open(file_path) as file_handle:
        lines = file_handle.readlines()
        for line in lines:
            line = line.strip()
            if line.__len__() and line[0] != '#':
                key_value = line.split(": ")
                ProSet[key_value[0]] = key_value[1]

    if ProSet["LibType"].lower() == "shared":
        ProSet["LibType"] = "True"
    else:
        ProSet["LibType"] = "False"


    return ProSet

def GetDeps(src_dic):
    deps_dic = {}
    for key in src_dic.keys():
        if "DepsOn" in key:
            info_list = src_dic[key].split(":")
            key = info_list[0].split("/")[0]
            version_value = info_list[1]
            shared_value = info_list[2]
            buildtype_value = info_list[3]
            if shared_value.lower() == "shared":
                shared_value = "True"
            else:
                shared_value = "False"
            deps_dic[key] = [version_value, shared_value, buildtype_value]
    return deps_dic #{libname: [version, shared]}

def GetDepsName(src_dic):
    deps_list = []
    for key in src_dic.keys():
        if "depson" in key.lower():
            info_list = src_dic[key].split(":")
            deps_name = info_list[0]
            deps_list.append(deps_name)
    return deps_list




def WriteProfile(src_dic, dst_file):
    config = ConfigParser.ConfigParser()
    config.add_section("settings")
    config.add_section("options")
    config.set("settings", "os", src_dic["OS"])
    config.set("settings", "arch", src_dic["Arch"])
    config.set("settings", "compiler", src_dic["Compiler"])
    config.set("settings", "compiler.version", src_dic["CompilerVersion"])
    config.set("settings", "compiler.libcxx", "libstdc++")
    config.set("settings", "build_type", src_dic["BuildType"])

    config.set("options", "*:shared", src_dic["LibType"])

    deps_dic = GetDeps(src_dic)
    for lib_name in deps_dic.keys():
        c = lib_name + ":compiler";
        cv = lib_name + ":compiler.version"
        s = lib_name + ":shared"
        b = lib_name + ":build_type"
        version = deps_dic[lib_name][0]
        shared = deps_dic[lib_name][1]
        buildtype = deps_dic[lib_name][2]

        config.set("settings", c, src_dic["Compiler"])
        config.set("settings", cv, version)
        config.set("settings", b, buildtype)
        config.set("options", s, shared)


    with open(dst_file, 'w') as profile:
        config.write(profile)
        profile.write("\n\n[build_requires]\n")
        for deps_name in GetDepsName(src_dic):
            profile.write(deps_name + "\n")



def WriteConanfile(src_dic, dst_file):
    with open(dst_file, 'w') as profile:
        profile.write("[requires]\n")
        for key in src_dic.keys():
            if "DepsOn" in key:
                profile.write(src_dic[key].split(":")[0])
                profile.write("\n")

        profile.write("\n\n[generators]\ncmake\n")


# g_proset = ReadProperty("../build.property")
# g_data = g_proset["Install"].split("@")
# g_lib_name = g_data[0].split("/")[0]
# g_lib_version = g_data[0].split("/")[1]
# g_author = g_data[1].split("/")[0]
# g_channel = g_data[1].split("/")[1]


if __name__ == "__main__":
    proset = ReadProperty("../build.property")
    WriteProfile(proset, "./.profile")
    WriteConanfile(proset, "./.conanfile")

    install_info = proset["Install"]
    print install_info