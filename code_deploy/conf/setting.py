# encoding:utf-8

prod_host_config = {
    "env": "prod",
    "hosts_list": ["10.10.10.30", ],
    "nodeName_list": ["linux-node3",],
    "port": 22,
    "user": "root",
    "pkey_file": "/root/.ssh/id_rsa",
}

pre_host_config = {
    "env": "pre",
    "hosts_list": ["10.10.10.30", ],
    "nodeName_list": ["linux-node3",],
    "port": 22,
    "user": "root",
    "pkey_file": "/root/.ssh/id_rsa",
}

log_dir = "/deploy/tmp/"
err_log_file = "/deploy/tmp/err.log"


svn_config = {
    "svn_url": "svn://192.168.1.221/",
    "svn_user": "deploy",
    "svn_pass": "123",
}

deploy_config = {
    "svn_checkout_dir": "/deploy/code",
    "deploy_tmp": "/deploy/tmp",
    "prod_tmp": "/data/website/prod_tmp",
    "web_root": "/data/website",
    "config_dir": "/deploy/config",
    "webuser": "nginx",
    "webuser_group": "nginx",
}

tar_config = {
    "tar_srcdir": "/deploy/code/",
    "tar_dstdir": "/data/website/deploy_tmp",
}

webtest_config = {
    "login_url": "http://crm.test.com/login.html",
    "post_url": "http://crm.test.com/login.html",
    "post_data": {
        'username': 'admin',
        'password': '123',
        'verify': 'undefined',
    },
    "test_url": "http://crm.test.com/index.html",
    "keyword": r"项目",
}
