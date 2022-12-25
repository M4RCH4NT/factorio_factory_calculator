import dash_cytoscape as cyto
from dash import Dash, html
import json


def Calculate_Manufacturing_Speed(Component):

    return Component["manu_time"]/Component["manu_amount"]


def Calculate_Required_Manufacturing_Of_Component(Component, Amount_Per_Second=1):

    return Calculate_Manufacturing_Speed(Component)*Amount_Per_Second


def Calculate_Required_Manufacturing(Component, Configuration, Components, Production, Results, Parent, Component_Name, Amount_Manu, Amount_Per_Second=1, depth=0, height=0, horizontal_scale=400, verticale_scale=300):

    Default_Recipe = Component["default"]

    Prefered_Recipe = Configuration["preferred_recipe"]

    if Component_Name in Prefered_Recipe.keys():
        Default_Recipe = Prefered_Recipe[Component_Name]

    try:
        Recipe = Component[Default_Recipe]["recipe"]
    except:
        Default_Recipe = Component["default"]
        Recipe = Component[Default_Recipe]["recipe"]

    Label = Component_Name

    Default_Recipe = Components[Component_Name]["default"]

    Manufacturing_Type = Components[Component_Name][Default_Recipe]['manu_type']


    try:
        temp_Production = Production[Manufacturing_Type][Configuration[Manufacturing_Type]]
    except:
        temp_Production = Production[Manufacturing_Type][Production[Manufacturing_Type]["default"]]

    Adjusted_Manu_Amount = Amount_Manu / \
                           temp_Production

    Optional_Recipes = ""

    Counter = 0

    if Configuration["show_optional_recipes"] == True:
        for Optional_Recipe in Components[Component_Name]:
            if (Optional_Recipe != "default") and (Optional_Recipe != Default_Recipe):
                Optional_Recipes = Optional_Recipes + "    " + Optional_Recipe + "\n"
                Counter += 1
    try:
        temp_Configuration = Configuration[Manufacturing_Type]
    except:
        # temp_Configuration = "default"
        temp_Configuration = Production[Manufacturing_Type]["default"]

    if Counter > 0:
        Data_Label = f"Component Name: {Label} \n Used Recipe: {Default_Recipe} \n Created In: {temp_Configuration} \n Amount: {round(Adjusted_Manu_Amount*100)/100}\n Optional Recipes:\n{Optional_Recipes}"
    else:
        Data_Label = f"Component Name: {Label} \n Used Recipe: {Default_Recipe} \n Created In: {temp_Configuration} \n Amount: {round(Adjusted_Manu_Amount*100)/100}"

    Results.append(
        {'data': {'id': Parent, 'label': Data_Label},
            'position': {'x': depth*horizontal_scale, 'y': height*verticale_scale}}
    )

    # Results.append(
    #     {'data': {'id': Parent, 'label': f"{Label} \n {Default_Recipe} \n {Manufacturing_Type} \n {round(Adjusted_Manu_Amount*100)/100}"},
    #         'position': {'x': depth*horizontal_scale, 'y': height*verticale_scale}}
    # )

    new_height = height
    return_height = height

    for Item in Recipe:

        try:

            Item_Default_Recipe = Components[Item[0]]["default"]

            Prefered_Recipe = Configuration["preferred_recipe"]

            if Item[0] in Prefered_Recipe.keys():
                Item_Default_Recipe = Prefered_Recipe[Item[0]]

            try:
                Check_Recipe = Components[Item[0]
                                          ][Item_Default_Recipe]["recipe"]
            except:
                Item_Default_Recipe = Components[Item[0]]["default"]

            Adjusted_Pass_Through = Amount_Per_Second * \
                Item[1] / Components[Component_Name][Default_Recipe]['manu_amount']

            required_manu_speed = Calculate_Required_Manufacturing_Of_Component(
                Components[Item[0]][Item_Default_Recipe], Adjusted_Pass_Through)

            # print(
            #     "-"*depth, Item[0], f" - amount {Components[Item[0]][Item_Default_Recipe]['manu_type']} = ", required_manu_speed, " --- ", new_height)

            Results.append(
                {'data': {'source': Parent + "_" + Item[0], 'target': Parent}})

            Results, return_height = Calculate_Required_Manufacturing(
                Components[Item[0]], Configuration, Components, Production, Results, Parent + "_" + Item[0], Item[0], required_manu_speed, Amount_Per_Second=Adjusted_Pass_Through, depth=depth + 1, height=new_height, horizontal_scale=horizontal_scale, verticale_scale=verticale_scale)

            new_height = return_height

        except:

            Results.append(
                {'data': {'source': Parent + "_" + Item[0], 'target': Parent}})
            Results.append(
                {'data': {'id': Parent + "_" + Item[0], 'label': Item[0]},
                    'position': {'x': (depth + 1) * horizontal_scale, 'y': new_height * verticale_scale}}
            )

        new_height = new_height + 1

    return Results, return_height

###################### Configuration ##############################


Component_File = "components.json"
Production_File = "production.json"

Target_Construction = "utility_tech_card"
Amount_Per_Second = 1

Configuration = {

    "assembling_machine": "assembling_machine_1",
    "furnace": "stone_furnace",
    "miner": "electric_drill",
    "oil_refinery": "oil_refinery_1",
    "offshore_pump": "offshore_pump_1",
    "filtration_plant": "filtration_plant_1",
    "crusher": "crusher_1",
    "chemical_plant": "chemical_plant_1",
    "show_optional_recipes": False,

    "preferred_recipe": {
    }

}

vertical_spacing = 150
horizontal_spacing = 300

###################### Generate Elements ##########################

f = open(Component_File, "r")
x = f.read()
Components = json.loads(x)
f.close()

f = open(Production_File, "r")
x = f.read()
Production = json.loads(x)
f.close()

Default_Recipe = Components[Target_Construction]["default"]

Prefered_Recipe = Configuration["preferred_recipe"]

if Target_Construction in Prefered_Recipe.keys():
    Default_Recipe = Prefered_Recipe[Target_Construction]
try:
    Check_Recipe = Components[Target_Construction][Default_Recipe]
except:
    Default_Recipe = Components[Target_Construction]["default"]

Component = Components[Target_Construction][Default_Recipe]

Results = []

required_manu_speed = Calculate_Required_Manufacturing_Of_Component(
    Component, Amount_Per_Second)
Results, height = Calculate_Required_Manufacturing(
    Components[Target_Construction], Configuration, Components, Production, Results, Target_Construction, Target_Construction, required_manu_speed, Amount_Per_Second, verticale_scale=vertical_spacing, horizontal_scale=horizontal_spacing)

Label = Target_Construction
Manufacturing_Type = Component['manu_type']

try:
    temp_Production = Production[Manufacturing_Type][Configuration[Manufacturing_Type]]
except:
    temp_Production = Production[Manufacturing_Type][Production[Manufacturing_Type]["default"]]

Adjusted_Manu_Amount = required_manu_speed / \
                       temp_Production

Optional_Recipes = ""

Counter = 0

if Configuration["show_optional_recipes"] == True:
    for Optional_Recipe in Components[Target_Construction]:
        if (Optional_Recipe != "default") and (Optional_Recipe != Default_Recipe):
            Optional_Recipes = Optional_Recipes + "    " + Optional_Recipe + "\n"
            Counter += 1

try:
    temp_Configuration = Configuration[Manufacturing_Type]

except:
    temp_Configuration =  Production[Manufacturing_Type]["default"]

if Counter > 0:
    Data_Label = f"Component Name: {Label} \n Used Recipe: {Default_Recipe} \n Created In: {temp_Configuration} \n Amount: {round(Adjusted_Manu_Amount*100)/100}\n Optional Recipes:\n{Optional_Recipes}"
else:
    Data_Label = f"Component Name: {Label} \n Used Recipe: {Default_Recipe} \n Created In: {temp_Configuration} \n Amount: {round(Adjusted_Manu_Amount*100)/100}"

Results[0] = {'data': {'id': Target_Construction, 'label': Data_Label},
              'position': {'x': 0, 'y': (height/2)*vertical_spacing}, 'align-items': "left", 'justify-content': 'left'}

# Results[0] = {'data': {'id': Target_Construction, 'label': f"{Label} \n {Default_Recipe} \n{Manufacturing_Type} \n {round(Adjusted_Manu_Amount*10)/10}"},
#               'position': {'x': 0, 'y': (height/2)*100}}


###################### Display Results ############################

app = Dash(__name__)

app.layout = html.Div([
    html.P("Dash Cytoscape:"),
    cyto.Cytoscape(
        id='cytoscape',
        elements=Results,
        # layout={'name': 'klay', 'fontsize': 10},
        layout={'name': 'preset'},
        style={'width': '1920px', 'height': '900px',
               'align-items': "left", 'text-halign': 'left'},
        stylesheet=[
            {'selector': 'edge', 'style': {'label': 'data(label)'}},
            {'selector': 'node', 'style': {
                'label': 'data(label)', 'text-wrap': 'wrap', 'align-items': "left", 'text-halign': 'right'}}
        ]
    )
])

app.run_server(debug=True)
