


from pro_craft.code.manager import CoderTemplateManager,Base


def test_connection():
    CoderTemplateManager( #mysql是无法使用的, 但是pg可以
        # database_url = "mysql:1234@192.168.8.165:3306/serverz",
        database_url="zxf_root:Zhf4233613%40@rm-2ze0793c6548pxs028o.mysql.rds.aliyuncs.com:3306/serverz",
        q_collection = "template_collection",
        q_host = "192.168.1.165",
        q_port = 6333,
        embed_model_name = "doubao-embedding-text-240715",
        embed_api_key = "39ad310a-c6f7-4d66-962e-1fbfa7e6edf1",
    )


def test_connection2():
    CoderTemplateManager(
        # database_url = "mysql:1234@192.168.8.165:3306/serverz",
        # postgresql://user:password@host:port/database_name,
        database_url = "ai:ai@192.168.1.165:5432/ai",
        # database_url="zxf_root:Zhf4233613%40@rm-2ze0793c6548pxs028o.mysql.rds.aliyuncs.com:3306/serverz",
        q_collection = "template_collection",
        q_host = "192.168.1.165",
        q_port = 6333,
        embed_model_name = "doubao-embedding-text-240715",
        embed_api_key = "39ad310a-c6f7-4d66-962e-1fbfa7e6edf1",
    )
