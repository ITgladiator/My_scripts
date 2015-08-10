#简单的代码发布脚本
@(架构)
##说明
目前业务还比较简单，并且需要频繁的发布，所以写了个脚本，简化自己的工作：
- **代码发布**：支持对多台服务器并发发布
- **代码回滚**：支持版本查看和代码回滚
- **代码测试**：发布完成后调用测试脚本自动测试

##发布流程

###流程图
![Alt text](/images/deploy.png)

###发布过程
1. 从SVN服务器checkout到本地
2. 添加版本标识并打包
3. 推送到正式服务器
4. 在正式服务器解压并做软链接到网站根目录
5. 测试网站状态（模拟登录）
6. 部署完成

##执行测试
###执行发布
```
[root@c66-3 code_deploy]# python deploy.py deploy
begin svn checkout...
Svn checkout sucessfull
src_dir = /deploy/code/cms
tar_dir = /deploy/tmp/prod_cms_1362_2015-08-05-03-23
begin tar...
OK! The codes tar sucessfull!
Filename : /deploy/tmp/prod_cms_1362_2015-08-05-03-23.tar.gz
begin send, untar file and make soft_link...
OK! Send file to 10.10.10.30 sucessfull!
OK! Untar file on 10.10.10.30 sucessfull!
OK! Make soft_link on 10.10.10.30 sucessfull!
OK! Send file to 10.10.10.40 sucessfull!
OK! Untar file on 10.10.10.40 sucessfull!
OK! Make soft_link on 10.10.10.40 sucessfull!
OK! Web test sucessfull!
```
###版本查看
```
[root@c66-3 code_deploy]# python deploy.py rollback-list

Host: 10.10.10.30 
prod_cms_1362_2015-08-05-01-48
prod_cms_1362_2015-08-05-03-23
            

Host: 10.10.10.40 
prod_cms_1356_2015-08-04-18-07
prod_cms_1356_2015-08-04-18-13
prod_cms_1362_2015-08-05-01-48
prod_cms_1362_2015-08-05-03-23
 
```
###版本回滚
```
[root@c66-3 code_deploy]# python deploy.py rollback-pro 10.10.10.40 prod_cms_1356_2015-08-04-18-13
Begin web test...
OK! Web test sucessfull!
Rollback sucessfull!
The current version is prod_cms_1356_2015-08-04-18-13
```
 
