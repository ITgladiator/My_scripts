# encoding:utf-8

host_config = {
    "hosts_list": ["10.10.10.30", ],
    "port": 22,
    "user": "root",
    "pkey_file": "/Users/gladiator/.ssh/id_rsa",
}

log_file = "/Users/gladiator/deploy/tmp/current_ver.log"


svn_config = {
    "svn_url": "svn://192.168.1.221/cms",
    "svn_user": "deploy",
    "svn_pass": "x..18610876365..",
    "svn_library": "cms"
}

deploy_config = {
    "env": "prod",
    "svn_checkout_dir": "/Users/gladiator/deploy/code",
    "deploy_tmp": "/Users/gladiator/deploy/tmp",
    "prod_tmp": "/data/website/prod_tmp",
    "web_root": "/data/website",
    "config_dir": "/Users/gladiator/deploy/config",
}

tar_config = {
    "tar_srcdir": "/Users/gladiator/deploy/code/cms",
    "tar_dstdir": "/Users/gladiator/data/website/deploy_tmp",
}

webtest_config = {
    "login_url": "http://crm.fcgtech.com/admin/public/login.html",
    "post_url": "http://crm.fcgtech.com/admin/public/login.html?s=/Admin/public/login.html",
    "post_data": {
        'username': 'admin',
        'password': '111111',
        'verify': 'undefined',
    },
    "test_url": "http://crm.fcgtech.com/crm/companion/index.html",
    "keyword": r"项目",
}