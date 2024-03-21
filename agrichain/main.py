from prettytable import PrettyTable


class Item:
    def __init__(self, tag, name, price, discount=None):
        self.tag = tag
        self.name = name
        self.price = price
        self.discount = discount if discount else {}

    def __str__(self):
        return f"Item(tag={self.tag}, name={self.name}, price={self.price}, discount={self.discount})"


class Cart:
    def __init__(self):
        self.items = []
        self.user_input = ""
        self.user_input_count_map = {}
        self.cart_items = []

    def get_items(self):
        return self.items

    def add_item(self, item):
        new_item = Item(item["tag"], item["name"],
                        item["price"], item.get("discount"))
        self.items.append(new_item)

    def __validate_and_merge(self):
        # invalid_items = [c for c in list(
        #     self.user_input) if c.islower() or c.isnumeric()]
        # if invalid_items:
        #     raise ValueError("Invalid input")
        # self.user_input_count_map = {key: self.user_input.count(
        #     key) for key in set(self.user_input)}

        # def __check_valid_inputs(self):
        arr = list(self.user_input)
        invalid_items = []
        for c in arr:
            if c.islower():
                invalid_items.append(c)
                print(f"Invalid: {c} Input is lowercase")
                exit(0)

            if c.isnumeric():
                invalid_items.append(c)
                print(f"Invalid: {c} Input is a number")
                exit(0)

        if len(invalid_items):
            exit(0)
        else:
            pass

        # def __validate_input_and_merge(self):
        input = self.user_input
        # exit(0) if self.__check_valid_inputs() is False else None
        merged_with_count = {}
        input_arr = list(input)
        for i in input_arr:
            key = i
            if key in merged_with_count:
                merged_with_count[key] = merged_with_count[key] + 1
            else:
                merged_with_count[key] = 1
        self.user_input_count_map = merged_with_count

    def __start_checkout(self):
        self.__validate_and_merge()

    def __price_queue(self):
        tag = "tag"
        discount = "discount"
        price = "price"
        sprice = "special_price"
        quantity = "quantity"

        item = self.get_items()
        input_map = self.user_input_count_map
        co_queue = []

        for item in self.get_items():
            if item.tag in input_map:
                items_count = input_map[item.tag]
                item_price = item.price

                if discount and sprice in item.discount and quantity in item.discount:
                    discount_quantity = item.discount[quantity]
                    discount_special_price = item.discount[sprice]

                    remainder_items = items_count % discount_quantity
                    discounted_items_total = items_count - remainder_items

                    discounted_groups_count = discounted_items_total / discount_quantity

                    discounted_groups_price = discounted_groups_count * discount_special_price

                    remainder_items_price = item_price * remainder_items

                    final_amount = discounted_groups_price + remainder_items_price
                    co_queue.append(final_amount)
                    self.cart_items.append({
                        "Tag": item.tag,
                        "Price": item.price,
                        "Quantity": input_map[item.tag],
                        "Discount": (items_count * item_price) - final_amount,
                        "Total": final_amount
                    })

                # elif item.discount[sprice] is None:
                else:
                    final_amount = item_price * items_count
                    co_queue.append(final_amount)
                    self.cart_items.append({
                        "Tag": item.tag,
                        "Price": item.price,
                        "Quantity": input_map[item.tag],
                        "Discount": 0,
                        "Total": final_amount
                    })

        return co_queue

    def checkout(self):
        uinp = input("Add Items to cart: ")
        self.user_input = uinp
        self.__start_checkout()
        price_list = self.__price_queue()
        cart_total = sum(price_list)
        print("Cart total: ", cart_total)
        print("Cart Bill: ", self.cart_items)


def main():
    apple = {
        "tag": "A",
        "name": "Apple",
        "price": 50,
        "discount": {"special_price": 130, "quantity": 3}
    }
    banana = {
        "tag": "B",
        "name": "Banana",
        "price": 30,
        "discount": {"special_price": 45, "quantity": 2}
    }
    cherry = {
        "tag": "C",
        "name": "Cherry",
        "price": 20
    }
    date = {
        "tag": "D",
        "name": "Date",
        "price": 15
    }
    cart = Cart()
    cart.add_item(apple)
    cart.add_item(banana)
    cart.add_item(cherry)
    cart.add_item(date)
    all_cart_items = cart.get_items()

    table = PrettyTable(
        field_names=["Item", "Unit Price", "Special Price"], align="l")

    for item in cart.get_items():
        tag_cell = item.tag
        price_cell = item.price
        discount_cell = ""
        discount = item.discount
        # if item["discount"]["quantity"] and item["discount"]["special_price"]:
        if discount and "special_price" in discount and "quantity" in discount:
            sprice = discount["special_price"]
            qty = discount["quantity"]
            discount_cell = f"{str(qty)} for {str(
                sprice)}" if sprice != 0 and qty != 0 else ""

        table.add_row([tag_cell, price_cell, discount_cell])
    print(table)

    try:
        cart.checkout()
    except KeyboardInterrupt:
        print("\nCancelled...")


if __name__ == "__main__":
    main()
