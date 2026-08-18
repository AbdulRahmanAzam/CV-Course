class GroceryManager:
  def __init__(self):
    self.items = {}

  def add_item(self, item, quantity, price):
    self.items[item] = {
        "quantity":quantity
        "price":price
        }
      print(f"{quantity} {item}(s) added to the grocery list.")

    def remove_item(self, item):
      if item in self.items:
        del self.items[item]
        print(f"{item} removed from the grocery list.")
      else:
        print(f"{item} is not in the grocery list.")
      
    def view_list(self):
      if not self.items:
        print("The grocery list is empty.")
      else:
        print("Grocery List:")
        for item, details in self.items.items():
          print(f"{details['quantity']} {item}(s) - ${details['price']} each")
    
    def calculate_total(self):
      total = 0
      for info in self.items.values():
        total += info["quantity"] * info["price"]
      

manager = GroceryManager()

manager.add_item("Apples", 3, 0.50)
manager.add_item("Milk", 2, 2.50)

manager.view_list()

print(f"\nTotal Cost: ${manager.calculate_total():.2f}")

# Testing error handling
manager.remove_item("Bread")  # Tries to remove an item that doesn't exist
manager.remove_item("Apples")  # Successfully removes an item

print(f"New Total Cost: ${manager.calculate_total():.2f}")





