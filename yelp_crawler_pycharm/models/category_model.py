from models import base_model


class Category(base_model.Base):

    Element_Class_Name = 'js-browse-businesses_category'

    def get_categories(self):
        result = []
        index = 0
        for elm in self.get_content(self.Base_Url).find_all('a', {'class': self.Element_Class_Name}):
            category = {}
            h3_tag = elm.find('h3')
            category['id'] = index
            category['name'] = h3_tag.string
            category['label'] = elm.get('data-analytics-label')
            if category['label'] == 'show_more':
                continue
            index += 1
            result.append(category)
        for elm in self.get_content(self.Base_Url).find_all('div', {'class': self.Element_Class_Name}):
            category = {}
            a_tag = elm.find('a')
            category['id'] = index
            category['name'] = a_tag.string
            category['label'] = elm.get('data-analytics-label')
            index += 1
            result.append(category)
        return result

