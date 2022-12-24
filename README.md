# factorio_factory_calculator

Basic Description:

Code to display a graph representing the required amount of factory modules and materials to produce the target item at a set speed in the game factorio.

How to use:

The components.json needs to contain all the components and their manufacturing information and recipes to create the component. The production.json contains descriptions of the factory modules and their information to create the components. Within the calculate_parts.py file, the target item, the wanted production speed (item/second), and configuration is specified. Running the program starts a server, and within the terminal the address can be found where the graph can be viewed in a local browser. 

Components.json:

The components.json file contains entries in the following format:

"<component name>" : {
  "default" : <default recipe name that should be used> ,
  "<recipe name>" : }
    "manu_type": <name of factory module type>,
    "manu_time": <seconds it takes for a batch of components>,
    "manu_amount": <amount of components made in a batch>,
    "recipe": [[<name of component in recipe>, <amount of components>], [<name of component in recipe>, <amount of components>], ...]
  },
  "<recipe name>" : }
    "manu_type": <name of factory module type>,
    "manu_time": <seconds it takes for a batch of components>,
    "manu_amount": <amount of components made in a batch>,
    "recipe": [[<name of component in recipe>, <amount of components>], [<name of component in recipe>, <amount of components>], ...]
  },
  ...
}

Production.json :

The production.json file contains the entries in the following format:

"<factory module type>": {
  "<factory module name>": <module manufacturing speed>,
  "<factory module name>": <module manufacturing speed>,
  ...
}
  
 Configuration:
 
 Within the calculate_parts.py, a dictionary variable called Configuration can be found where the configuration is set. The format is as follows:
 
 Configuration = {
  
    # Set the wanted factory module that should be used to construct the corresponding components.    
    "<factory module type>": <factory module name>, 
    "<factory module type>": <factory module name>,
    ...,
    
    # True or False whether the names of optional recipes should be shown at the output.
    "show_optional_recipes": False, 
    
    # Set which recipe should be used to contruct component, otherwise default recipe will be used.
    "preferred_recipe": {
      "<name of component>" : "<name of recipe>"
    }

}
