from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self, current_page, data_count, per_page_article_num = 10, pager_num = 7):
        '''
        
        :param current_page:            当前页
        :param data_count:              数据库里存的文章总数
        :param per_page_article_num:    每页要显示的文章数
        :param pager_num:               每页要显示的页码标签数
        '''
        
        try:
            self.current_page = int(current_page)
        except Exception as e:
            self.current_page = 1           

        self.data_count = data_count        
        self.per_page_article_num = per_page_article_num    
        self.pager_num = pager_num         

    @property
    def start(self):
        # 每页从数据库获取从哪条开始取
        return (self.current_page - 1) * self.per_page_article_num

    @property
    def end(self):
        # 取到哪里
        return (self.current_page) * self.per_page_article_num

    @property
    def total_num(self):
        # 总页数：文章总数/每页显示文章数
        value, y = divmod(self.data_count, self.per_page_article_num)   # value是商(页数)， y是余数，如果有余数，总页数多加1页
        if y:
            value += 1
        return value

    def page_str(self, base_url):
        page_list = []      # 要显示在前端页面的文本

        if self.total_num < self.pager_num:         # 如果【总页数】 < 【要显示页码标签数】（标签显示7页，但是总页数只有2页）
            start_index = 1
            end_index = self.total_num + 1

        elif (self.current_page + (self.pager_num + 1)/2) > self.total_num:
            start_index = self.total_num - self.pager_num + 1
            if start_index <= 0:
                start_index = 1
                
            end_index = self.total_num + 1
        else:
            start_index = self.current_page - (self.pager_num + 1)/2
            if start_index <= 0:
                start_index = 1
                # end_index =

            end_index = self.current_page + (self.pager_num + 1)/2
        start_index = int(start_index)
        end_index = int(end_index)

        #### 生成上一页标签
        if self.current_page == 1:
            prev = '<li class="disabled"><a href="javascript:void(0);" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
        else:
            prev = '<li><a href="%s?p=%s" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li' %(base_url, self.current_page-1)
        page_list.append(prev)


        #### 生成页码标签
        for i in range(start_index, end_index):
            if i == self.current_page:
                temp = '<li class="active"><a href="%s?p=%s">%s<span class="sr-only">(current)</span></a></li>' %(base_url, i, i,)
            else:
                temp = '<li><a href="%s?p=%s">%s<span class="sr-only">(current)</span></a></li>' %(base_url, i, i,)
            page_list.append(temp)
        
        
        #### 生成下一页标签
        if self.current_page == self.total_num:
            nex = '<li class="disabled"><a href="javascript:void(0);" aria-label="Next"><span aria-hidden="true">»</span></a></li'
        else:
            nex = '<li><a href="%s?p=%s" aria-label="Next"><span aria-hidden="true">»</span></a></li' %(base_url, self.current_page+1)

        page_list.append(nex)
        
        p_str = mark_safe(''.join(page_list))
        
        return p_str

            