import module_extractor
import neo4j_driver

# 设置图及坐标
# fig, ax = plt.subplots(1, 1, figsize=(10, 10))
# ax.set_xlim(-20000, 20000)
# ax.set_ylim(-20000, 20000)
# ax.set_aspect('equal')

# 设置拥有各个模块类实例信息的列表,这一步是把从ifc中提取出来的信息转化到类实例里
# existing_basic_list = BasicModule.BasicModule.basic_list_existing()
# existing_corridor_list = CorridorModule.CorridorModule.corridor_list_existing()
# existing_conjunct_list = ConjunctiveModule.ConjunctiveModule.conjunct_list_existing()
# existing_tube_list = TubeModule.TubeModule.tube_list_existing()

# 如果我想删除了
# del basicModule
# 显示模块
# if 'basicModule' in locals():
# basicModule.show_basicModule()

# 应用shapely package 显示图形
# for basic in existing_basic_list:
# basic.show_basic_module()
# for corridor in existing_corridor_list:
# corridor.show_corridor_module()
# for conjunct in existing_conjunct_list:
# conjunct.show_conjunctive_module()
# existing_tube_list[0].show_tube()
# plt.show()

a = module_extractor.ModuleExtractor('MA.ifc')
tube_id = a.get_tube_id()
corridor_id = a.get_corridor_id()
basic_id = a.get_basic_id()
conjunct_id = a.get_conjunct_id()
tube_basic_adjacency = a.get_tube_basic_adjacency()
tube_conjunct_adjacency = a.get_tube_conjunct_adjacency()
tube_corridor_adjacency = a.get_tube_corridor_adjacency()
basic_conjunct_adjacency = a.get_basic_conjunct_adjacency()
corridor_basic_adjacency = a.get_corridor_basic_adjacency()
corridor_conjunct_adjacency = a.get_corridor_conjunct_adjacency()
corridor_adjacency = a.get_corridor_adjacency()
basic_adjacency = a.get_basic_adjacency()
conjunct_adjacency = a.get_conjunct_adjacency()
corridor_house_connectivity = a.get_corridor_house_connectivity()
house_connectivity = a.get_house_connectivity()


# docker启动 neo4j
scheme = "bolt"
host_name = "localhost"
port = 7687
url = f"{scheme}://{host_name}:{port}"
username = "neo4j"
password = "Xyz0531!"
app = neo4j_driver.App(url, username, password)

# 将类实例中的信息导入neo4j中
for global_id in tube_id:
    app.add_tube_module(global_id)
for global_id in corridor_id:
    app.add_corridor_module(global_id)
for global_id in basic_id:
    app.add_basic_module(global_id)
for global_id in conjunct_id:
    app.add_conjunctive_module(global_id)

for i in range(len(tube_basic_adjacency)):
    if tube_basic_adjacency[i][2] == 1:
        app.add_tube_basic_adjacency(tube_basic_adjacency[i][0], tube_basic_adjacency[i][1])

for i in range(len(tube_conjunct_adjacency)):
    if tube_conjunct_adjacency[i][2] == 1:
        app.add_tube_conjunct_adjacency(tube_conjunct_adjacency[i][0], tube_conjunct_adjacency[i][1])

for i in range(len(tube_corridor_adjacency)):
    if tube_corridor_adjacency[i][2] == 1:
        app.add_tube_corridor_adjacency(tube_corridor_adjacency[i][0], tube_corridor_adjacency[i][1])

for i in range(len(corridor_adjacency)):
    if corridor_adjacency[i][2] == 1:
        app.add_corridor_adjacency(corridor_adjacency[i][0], corridor_adjacency[i][1])

for i in range(len(corridor_basic_adjacency)):
    if corridor_basic_adjacency[i][2] == 1:
        app.add_corridor_basic_adjacency(corridor_basic_adjacency[i][0], corridor_basic_adjacency[i][1])

for i in range(len(corridor_conjunct_adjacency)):
    if corridor_conjunct_adjacency[i][2] == 1:
        app.add_corridor_conjunct_adjacency(corridor_conjunct_adjacency[i][0], corridor_conjunct_adjacency[i][1])

for i in range(len(basic_adjacency)):
    if basic_adjacency[i][2] == 1:
        app.add_basic_adjacency(basic_adjacency[i][0], basic_adjacency[i][1])

for i in range(len(conjunct_adjacency)):
    if conjunct_adjacency[i][2] == 1:
        app.add_conjunct_adjacency(conjunct_adjacency[i][0], conjunct_adjacency[i][1])

for i in range(len(basic_conjunct_adjacency)):
    if basic_conjunct_adjacency[i][2] == 1:
        app.add_basic_conjunct_adjacency(basic_conjunct_adjacency[i][0], basic_conjunct_adjacency[i][1])

for i in range(len(corridor_id)):
    app.add_tube_corridor_connectivity(tube_id[0], corridor_id[i])

for i in range(len(corridor_house_connectivity)):
    if corridor_house_connectivity[i][1] in basic_id:
        app.add_corridor_basic_connectivity(corridor_house_connectivity[i][0],corridor_house_connectivity[i][1])
    elif corridor_house_connectivity[i][1] in conjunct_id:
        app.add_corridor_conjunct_connectivity(corridor_house_connectivity[i][0],corridor_house_connectivity[i][1])

for i in range(len(house_connectivity)):
    if house_connectivity[i][0] in conjunct_id:
        app.add_conjunct_connectivity(house_connectivity[i][0], house_connectivity[i][1])
    elif house_connectivity[i][0] in basic_id and house_connectivity[i][1] in conjunct_id:
        app.add_basic_conjunct_connectivity(house_connectivity[i][0], house_connectivity[i][1])
    else:
        app.add_basic_connectivity(house_connectivity[i][0], house_connectivity[i][1])
