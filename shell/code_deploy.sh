#!/bin/bash
#  deploy cms 
#  by guochao@20150715
#  v1.0

#svn
SVNUSER="deploy"
SVNPASS="123"
SVNURL="svn://192.168.1.22/cms"

#Date/Time
CDATE=$(date "+%Y-%m-%d")
CTIME=$(date "+%Y-%m-%d-%H-%M")

#Shell 
CODE_DIR="/deploy/code"
CONFIG_DIR="/deploy/config"
TMP_DIR="/deploy/tmp"
TAR_DIR="/deploy/tar"

usage(){
	echo $"Usage: $0 [deploy | rollback-list | rollback-pro ver]"
}

svn_pro(){
  echo -e "\033[31;1mbegin svn checkout\033[0m"
  cd $CODE_DIR && svn co $SVNURL --username=$SVNUSER --password=$SVNPASS
  cd $CODE_DIR/cms
  API_VER=$(svn info|grep Revision|awk '{print $2}')
  echo $API_VER >/server/scripts/tmp/deploy_version.log
  cp -r ${CODE_DIR}/cms "$TMP_DIR"
}

config_pro(){
  echo -e "\033[31;1madd pro config\033[0m"
  /bin/cp "$CONFIG_DIR"/Application/Crm/Conf/config.php $TMP_DIR/cms/Application/Crm/Conf/
  /bin/cp "$CONFIG_DIR"/Application/User/Conf/config.php $TMP_DIR/cms/Application/User/Conf/
  /bin/cp "$CONFIG_DIR"/Application/Common/Conf/config.php $TMP_DIR/cms/Application/Common/Conf/
  [ -d $TMP_DIR/cms/Application/Statistics/Conf/ ] || mkdir $TMP_DIR/cms/Application/Statistics/Conf/
  /bin/cp "$CONFIG_DIR"/Application/Statistics/Conf/config.php $TMP_DIR/cms/Application/Statistics/Conf/
  TAR_VER="$API_VER"_"$CTIME"
  cd $TMP_DIR && mv cms pro_cms_"$TAR_VER"
}

tar_pro(){
  echo -e "\033[31;1mbegin tar pro\033[0m"
  cd $TMP_DIR && tar czf pro_cms_"$TAR_VER".tar.gz pro_cms_"$TAR_VER"
  echo -e "\033[31;1mtar end pro_cms_"$TAR_VER".tar.gz\033[0m"
}

scp_pro(){
  echo -e "\033[31;1mbegin cp\033[0m"
  /bin/cp $TMP_DIR/pro_cms_"$TAR_VER".tar.gz /data/website/deploy_tmp

}

deploy_pro(){
  echo -e "\033[31;1mbegin deploy\033[0m"
  cd /data/website/deploy_tmp && tar zxf pro_cms_"$TAR_VER".tar.gz
  rm -f /data/website/cms
  ln -s /data/website/deploy_tmp/pro_cms_"$TAR_VER" /data/website/cms
  cd /data/website/cms
  [ -d Uploads/ ] && mv Uploads /tmp/Uploads.$CTIME
  [ -d data/ ] && mv data /tmp/data.$CTIME
  ln -s /data/website/Uploads /data/website/cms/Uploads
  ln -s /data/website/data /data/website/cms/data
  chown -R nginx.nginx /data/website/cms/
  cd /data/website/cms/ && sed -i s#"'APP_DEBUG', true"#"'APP_DEBUG', false"#g index.php
}

test_pro(){
  echo -e "\033[31;1mtest begin\033[0m"
  echo -e "\033[31;1mtest ok\033[0m"
}

rollback_list(){
  ls -l /data/website/deploy_tmp/*cms*.tar.gz
}

rollback_pro(){
   rm -f /data/website/cms
   ln -s /data/website/deploy_tmp/$1 /data/website/cms
   chown -R nginx.nginx /data/website/cms/
}

main(){
  case $1 in
    deploy)
	svn_pro;
	config_pro;
	tar_pro;
	scp_pro;
	deploy_pro;
	test_pro;
	;;
    rollback-list)
	rollback_list;
	;;
    rollback-pro)
	rollback_pro $2;
	;;
    *)
	usage;
    esac
}

main $1 $2
