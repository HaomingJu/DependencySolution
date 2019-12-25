import os
import sys
import ConfigParser
from conans import tools
from conans.client.conan_api import ConanAPIV1



compiler_version = "5"

def ReadProperty(file_path):
    ProSet = {}
    with open(file_path) as file_handle:
        lines = file_handle.readlines()
        for line in lines:
            line = line.strip()
            if line.__len__() and line[0] != '#':
                key_value = line.split(": ")
                ProSet[key_value[0]] = key_value[1]

    ProSet["RawLibType"] = ProSet["LibType"]
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
            # ['glog/0.4.0@Common/Release', 'Static', 'gcc_5.4']
            shared_value = info_list[1]
            version_value = compiler_version
            buildtype_value = info_list[1]

            if shared_value.lower() == "shared":
                shared_value = "True"
            else:
                shared_value = "False"
            deps_dic[key] = [version_value, shared_value, buildtype_value]
    return deps_dic #{libname: [version, shared]}

def GetDepsName(src_dic):
    deps_list = []
    general_list = []
    for key in src_dic.keys():
        if "depson" in key.lower():
            raw_info = src_dic[key].split(":")
            w_line = raw_info[0] + "/" +\
                    raw_info[1] + "-" +\
                    raw_info[2] + "-" +\
                    src_dic["OS"] + "-" +\
                    src_dic["Arch"] + "-" +\
                    raw_info[3]
            deps_list.append(w_line.strip())
        elif "general" in key.lower():
            w_line = src_dic[key].replace(":", "/")
            general_list.append(w_line.strip())
        else:
            pass
    return deps_list, general_list




def WriteProfile(src_dic, dst_file):
    config = ConfigParser.ConfigParser()
    config.add_section("settings")
    config.add_section("options")
    config.set("settings", "os", src_dic["OS"])
    config.set("settings", "arch", src_dic["Arch"])
    config.set("settings", "compiler", src_dic["Compiler"])
    # config.set("settings", "compiler.version", src_dic["CompilerVersion"])
    config.set("settings", "compiler.version", compiler_version)
    config.set("settings", "compiler.libcxx", "libstdc++")
    config.set("settings", "build_type", src_dic["BuildType"])

    config.set("options", "*:shared", src_dic["LibType"])

    deps_dic = GetDeps(src_dic)
    for lib_name in deps_dic.keys():
        # c = lib_name + ":compiler";
        # cv = lib_name + ":compiler.version"
        s = lib_name + ":shared"
        b = lib_name + ":build_type"
        # version = deps_dic[lib_name][0]
        version = compiler_version
        shared = deps_dic[lib_name][1]
        buildtype = deps_dic[lib_name][2]
        # config.set("settings", c, src_dic["Compiler"])
        # config.set("settings", cv, version)
        config.set("settings", b, buildtype)
        config.set("options", s, shared)


    with open(dst_file, 'w') as profile:
        config.write(profile)
        profile.write("\n\n[build_requires]\n")
        deps_list, general_list = GetDepsName(src_dic)
        for deps_name in deps_list:
            profile.write(deps_name + "\n")
        for general_name in general_list:
            profile.write(general_name + "\n")



def WriteConanfile(src_dic, dst_file, conanfile_py):
    deps_list, general_list = GetDepsName(src_dic)
    with open(dst_file, 'w') as profile:
        profile.write("[requires]\n")
        for deps in deps_list:
            profile.write(deps)
            profile.write("\n")
        for gen in general_list:
            profile.write(gen)
            profile.write("\n")

        profile.write("\n\n[generators]\ncmake\n")

    tools.replace_in_file(conanfile_py, "requires = \"\"", "requires = " + str(general_list + deps_list))

def InitConanRemote(proset):
    conan_remote_url = proset["JFrogURL"].split()[0]
    conan_uname = proset["UserName"].split()[0]
    conan_pwd = proset["Password"].split()[0]

    try:
        ConanAPIV1().remote_add("JFrogURL", conan_remote_url)
    except Exception as e:
        # print "The JFrogURL has been added"
        pass

    try:
        ConanAPIV1().users_clean()
        ConanAPIV1().user_set(conan_uname)
        ConanAPIV1().authenticate(conan_uname, conan_pwd, "JFrogURL")
    except Exception as e:
        pass



if __name__ == "__main__":
    proset = ReadProperty("../build.property")
    InitConanRemote(proset)
    WriteProfile(proset, "./.profile")
    WriteConanfile(proset, "./.conanfile", "./conanfile.py")

    install_info = None
    if proset["Type"].lower() == "library":
        install_info = proset["Install"] + "/" \
                + proset["BuildType"] + "-" \
                + proset["RawLibType"] + "-" \
                + proset["OS"] + "-" \
                + proset["Arch"] + "-" \
                + proset["Compiler"] + "-" \
                + proset["CompilerVersion"]
    else: # general
        install_info = proset["Install"] + "/" \
                + proset["Type"]

    print install_info
