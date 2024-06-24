from aimbots import testinglotAimbot

if __name__ == "__main__":

    bot = testinglotAimbot(

                    # 游戏窗体的名称
                    window_name= "Counter-Strike 2", 

                    # 选取的pytorch模型路径
                    model_path="./models/CS_150_epoch.pt",

                    # 普通模式和瞄准模式下准心位置初值（待会儿可以调整）
                    cross=[320, 337],
                    aim_cross=[320, 363],

                    # 普通模式和瞄准模式下的鼠标移动灵敏度
                    scaller=0.8,
                    aim_scaller=0.4,

                    # activeness 参数
                    activeness=500,
                    activeness_factor=12, 
                    activeness_trigger=7,

                    # 是否展现可视化窗口
                    visulize=True,

                    # 鼠标左键持续时间
                    click_delay=0.2 
            )

    # 准心校准
    bot.corss_align()

    # 运行
    bot.run()   
