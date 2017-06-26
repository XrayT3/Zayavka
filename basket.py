class Basket:
    sum_price = None
    items_num = None
    items = []

    def set_items(self, *args):         # на вход подается список готовых собранных объектов типа Item
        for item in range(args):        # input = list of Items objects
            self.items.append(item)     # no output
            self.items_num += 1
            self.sum_price += Item.get_price()

    def set_data_items(self, *args):     # на вход подается список , состоящий из структур данных типа Item.data_types
        for data in range(args):        # из каждой Item.data_types структуры собирается объект Item
            temp = Item()               # и переходит в основной список Basket.items[]
            temp.set_data(data)
            self.items.append(temp)
            temp.delete()


    def get_items(self):
        args = []
        for item in range(self.items):
            args.append((item.get_data()))
        return args

    def delete(self):
        self.sum_price = None
        self.items_num = None
        self.items = None


