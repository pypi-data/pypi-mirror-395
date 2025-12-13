import blazecache.blazecache as blazecache

if __name__ == "__main__":
    electron_repo_code_dir = {
        "aha-electron": "/Users/bytedance/Desktop/aha-electron/aha-electron"
    }
    electron_feature_branch = {
        "aha-electron": "v37",
    }
    fallback_branch = {
        "aha-electron": "v37"
    }
    mr_target_branch = {
        "aha-electron": "v37"
    }
    base_commit = {
        "aha-electron": "17e2ee2f663dcb38aa1598f79bf65bae32d7f1b4"
    }
    label_name = "mac_arm64_aha_ebbb66ec"
    bccache = blazecache.BlazeCache(product_name="electron-test", build_dir="/Users/bytedance/Desktop/aha-electron/aha-electron/",
                                    local_repo_dir=electron_repo_code_dir, os_type="macos arm64", branch_type="main", task_type="ci_check_task",
                                    machine_id="123456", ninja_exe_path="/Users/bytedance/Desktop/aha-electron/depot_tools/ninja",
                                    mr_target_branch=mr_target_branch, feature_branch=electron_feature_branch, p4_client="test-ci-check-electron", fallback_branch=fallback_branch, product_tos_url="https://tosv.byted.org/obj/blazecache-cn/product_config/aha-electron/product_config.json")
    bccache.run_precompile_plugin(mr_id="1234", base_commit=base_commit, label_name=label_name)
    # print(bccache.run_postcompile_plugin())