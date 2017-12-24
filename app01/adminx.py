from django_extra import xadmin
from  xadmin import views
from app01 import models

class BaseSetting:
    '''
    增加主题样式
    '''
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    '''
    修改标题

    '''
    site_title = "jeff后台管理系统"
    site_footer = "http://www.cnblogs.com/Jeffding/"
    menu_style = "accordion"#修改样式


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)




xadmin.site.register(models.Article)
xadmin.site.register(models.Article2Tag)
xadmin.site.register(models.ArticleDetail)
xadmin.site.register(models.Blog)
xadmin.site.register(models.Category)
xadmin.site.register(models.Comment)
xadmin.site.register(models.Tag)
xadmin.site.register(models.UpDown)
xadmin.site.register(models.UserFans)
xadmin.site.register(models.UserInfo)