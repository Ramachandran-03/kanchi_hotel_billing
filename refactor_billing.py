import re

def refactor_billing_screen():
    path = "r:\\Development\\kanchi_hotel_billing\\lib\\screens\\billing_screen.dart"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # We need to change the root build method of _BillingScreenState
    
    # 1. Remove the root providers
    target1 = """    final settings = Provider.of<SettingsProvider>(context).settings;
    final menuProvider = Provider.of<MenuProvider>(context);
    final orderProvider = Provider.of<OrderProvider>(context);
    final categoryProvider = Provider.of<CategoryProvider>(context);
    final cs = settings.currencySymbol;

    final availableItems = menuProvider.allItems
        .where((i) => i.isAvailable && i.stock > 0)
        .where((i) => _selectedCategory.isEmpty || i.category == _selectedCategory)
        .toList();"""
    new1 = """    // Providers moved down to Consumers for better performance"""
    content = content.replace(target1, new1)

    # 2. Update menuSection
    menu_section_current = """    final menuSection = Column(
      children: ["""
    
    menu_section_new = """    final menuSection = Consumer3<MenuProvider, CategoryProvider, SettingsProvider>(
      builder: (context, menuProvider, categoryProvider, settingsProv, _) {
        final cs = settingsProv.settings.currencySymbol;
        final availableItems = menuProvider.allItems
            .where((i) => i.isAvailable && i.stock > 0)
            .where((i) => _selectedCategory.isEmpty || i.category == _selectedCategory)
            .toList();

        return Column(
          children: ["""
    content = content.replace(menu_section_current, menu_section_new)
    
    # 3. Update the closing of menuSection (before cartSection)
    menu_section_end_current = """          ),
      ],
    );"""
    
    # Let's use regex for safer replacement if there are varying spaces
    menu_section_end_new = """          ),
          ],
        );
      },
    );"""
    content = content.replace(menu_section_end_current, menu_section_end_new)

    # 4. In menuSection, change the onTap function:
    # onTap: () => orderProvider.addItem(item),
    content = content.replace(
        "onTap: () => orderProvider.addItem(item),",
        "onTap: () => Provider.of<OrderProvider>(context, listen: false).addItem(item),"
    )

    # 5. Update cartSection
    # Since dart fix or manual changes might have altered indentation slightly, I'll be careful
    cart_section_current = """      margin: isTablet ? const EdgeInsets.all(16) : EdgeInsets.zero,
      child: Column(
        children: ["""
    
    cart_section_new = """      margin: isTablet ? const EdgeInsets.all(16) : EdgeInsets.zero,
      child: Consumer2<OrderProvider, SettingsProvider>(
        builder: (context, orderProvider, settingsProv, _) {
          final cs = settingsProv.settings.currencySymbol;
          return Column(
            children: ["""
    content = content.replace(cart_section_current, cart_section_new)

    cart_section_end_current = """                  ),
                ),
              ],
            ),
    );"""
    
    cart_section_end_new = """                  ),
                ),
              ],
            );
        },
      ),
    );"""
    content = content.replace(cart_section_end_current, cart_section_end_new)

    # 6. Update the AppBar actions
    actions_current = """        actions: [
          IconButton(
            icon: const Icon(Icons.settings_suggest, color: Colors.white),
            tooltip: 'Order Options',
            onPressed: _showOrderOptionsSheet,
          ),
          if (orderProvider.hasItems)
            TextButton.icon(
              onPressed: () => orderProvider.clearBill(),
              icon: const Icon(Icons.clear_all, color: Colors.white),
              label: const Text('Clear', style: TextStyle(color: Colors.white)),
            ),
        ],"""
        
    actions_new = """        actions: [
          IconButton(
            icon: const Icon(Icons.settings_suggest, color: Colors.white),
            tooltip: 'Order Options',
            onPressed: _showOrderOptionsSheet,
          ),
          Consumer<OrderProvider>(
            builder: (context, orderProv, _) {
              if (!orderProv.hasItems) return const SizedBox.shrink();
              return TextButton.icon(
                onPressed: () => orderProv.clearBill(),
                icon: const Icon(Icons.clear_all, color: Colors.white),
                label: const Text('Clear', style: TextStyle(color: Colors.white)),
              );
            },
          ),
        ],"""
    content = content.replace(actions_current, actions_new)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Refactored billing_screen.dart")

if __name__ == "__main__":
    refactor_billing_screen()
