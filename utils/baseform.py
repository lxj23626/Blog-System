class BaseForm(object):
    ''' 为了获取request，否则在自定义form的时候拿不到request '''
    
    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.userinfo = {}
        self.rmb = False
        super(BaseForm, self).__init__(*args, **kwargs)
