#                            ,,                      ,,    ,,
#   .M"""bgd mm            `7MM         `7MM"""Mq.   db  `7MM
#  ,MI    "Y MM              MM           MM   `MM.        MM
#  `MMb.   mmMMmm `7M'   `MF'MM  .gP"Ya   MM   ,M9 `7MM    MM  .gP"Ya
#    `YMMNq. MM     VA   ,V  MM ,M'   Yb  MMmmdM9    MM    MM ,M'   Yb
#  .     `MM MM      VA ,V   MM 8M""""""  MM         MM    MM 8M""""""
#  Mb     dM MM       VVV    MM YM.    ,  MM         MM    MM YM.    ,
#  P"Ybmmd"  `Mbmo    ,V   .JMML.`Mbmmd'.JMML.     .JMML..JMML.`Mbmmd'
#                    ,V
#                 OOb"
#
# A helper script for AUTOMATIC1111/stable-diffusion-webui.
# Enter your keywords and let the selections help you determine the look.
# https://replicate.com/methexis-inc/img2prompt has been an incredible help for improving the prompts.
# https://docs.google.com/document/d/1ZtNwY1PragKITY0F4R-f8CarwHojc9Wrf37d0NONHDg/ has been equally super important.
# Thanks to https://github.com/xram64 for helping fix the interface
# Art movements from https://en.wikipedia.org/wiki/List_of_art_movements I threw out the ones that did not work

# Portrait prompt - Portrait of an attractive young lady,flower field background, (by artist [X]:1.3), square ratio
# Negative - missing limbs, extra limbs

# Landscape prompt - Small house in the middle of a forest,near a lake
# Action prompt - Astronaut floating in space,firing laser at alien ship,galaxy background

# Negatives - watermark,label,text

# 20 steps on Euler A
# Seed - 669

import copy
import os
import random
from os import listdir, path
from os.path import isfile, join

import modules.scripts as scripts
import gradio as gr
from modules.processing import Processed, process_images
from modules.shared import cmd_opts, opts, state
from modules import scripts

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

ResourceDir = os.path.join(scripts.basedir(), f"StylePile/")

def FilesInFolder(SourceFolder):
    return [file for file in os.listdir(SourceFolder)]

def FilesInFolderFullPath(SourceFolder):
    return [SourceFolder + file for file in os.listdir(SourceFolder)]

ElementConcept = [
    "Acclaimed",
    "Alternative",
    "Amateur",
    "Artificial",
    "Award Winning",
    "Basic",
    "Beginner",
    "Bipolar",
    "Boyish",
    "Childish",
    "Cinematic",
    "Clever",
    "Clumsy",
    "Cognitive",
    "Complex",
    "Compressed",
    "Controllable",
    "Corrupted",
    "Damaged",
    "Destroyed",
    "Disgusting",
    "Divisive",
    "Dramatic",
    "Dumb",
    "Eliminated",
    "Excessive",
    "Exciting",
    "Extreme",
    "Feminine",
    "Filtered",
    "Fixated",
    "Fixed",
    "Foolish",
    "Fragile",
    "Girlish",
    "Gorgeous",
    "Groundbreaking",
    "Hated",
    "Hidden",
    "Highly Rated",
    "Horrifying",
    "Imaginary",
    "Imaginative",
    "Imitated",
    "Jaded",
    "Light hearted",
    "Loved",
    "Low Rated",
    "Magical",
    "Masculine",
    "Masterful",
    "Masterpiece",
    "Maximalist",
    "Methodological",
    "Misunderstood",
    "Mundane",
    "Overprocessed",
    "Pathetic",
    "Photoshopped",
    "Preview",
    "Raw",
    "Recycled",
    "Religious",
    "Rough",
    "Sacrificial",
    "Sacrilegious",
    "Schematic",
    "Simple",
    "Sophisticated",
    "Stupid",
    "Trustworthy",
    "Unbelievable",
    "Understandable",
    "Unearthed",
    "Unfiltered",
    "Unfinished",
    "Unhinged",
    "Universal",
    "Unsuccessful",
    "Venerable",
    "Visionary",
    "Vivacious"
]

ConceptMap = {
    "广受好评": "Acclaimed",
    "另类的": "Alternative",
    "业余": "Amateur",
    "人造的": "Artificial",
    "获奖": "Award Winning",
    "基础": "Basic",
    "初学者": "Beginner",
    "躁狂抑郁性精神病的": "Bipolar",
    "孩子气": "Boyish",
    "幼稚": "Childish",
    "电影": "Cinematic",
    "灵巧": "Clever",
    "笨拙": "Clumsy",
    "感知的": "Cognitive",
    "精密的": "Sophisticated",
    "压缩": "Compressed",
    "可控": "Controllable",
    "堕落": "Corrupted",
    "损坏的": "Damaged",
    "毁坏": "Destroyed",
    "恶心": "Disgusting",
    "分裂": "Divisive",
    "戏剧性": "Dramatic",
    "沉默": "Dumb",
    "淘汰": "Eliminated",
    "过多的": "Excessive",
    "激动人心": "Exciting",
    "极端": "Extreme",
    "女性化": "Feminine",
    "过滤": "Filtered",
    "固定": "Fixated",
    "固定的": "Fixed",
    "愚蠢": "Foolish",
    "脆弱的": "Fragile",
    "少女风": "Girlish",
    "华丽的": "Gorgeous",
    "开创性": "Groundbreaking",
    "讨厌": "Hated",
    "隐藏": "Hidden",
    "高度评价": "Highly Rated",
    "令人毛骨悚然": "Horrifying",
    "假想": "Imaginary",
    "想象力": "Imaginative",
    "模仿": "Imitated",
    "厌倦": "Jaded",
    "轻松愉快": "Light hearted",
    "爱过": "Loved",
    "低评级": "Low Rated",
    "神奇": "Magical",
    "男性": "Masculine",
    "大师级": "Masterful",
    "杰作": "Masterpiece",
    "极简主义": "Maximalist",
    "方法论": "Methodological",
    "不为人理解的": "Misunderstood",
    "世俗": "Mundane",
    "过度加工": "Overprocessed",
    "令人怜惜的": "Pathetic",
    "PS": "Photoshopped",
    "预览": "Preview",
    "原始": "Raw",
    "可回收": "Recycled",
    "宗教": "Religious",
    "粗糙的": "Rough",
    "牺牲": "Sacrificial",
    "亵渎": "Sacrilegious",
    "原理图": "Schematic",
    "简单的": "Simple",
    "愚蠢的": "Stupid",
    "值得信赖": "Trustworthy",
    "难以置信": "Unbelievable",
    "可以理解": "Understandable",
    "出土/异域魔影": "Unearthed",
    "未经过滤": "Unfiltered",
    "未完成": "Unfinished",
    "精神错乱": "Unhinged",
    "共同的": "Universal",
    "不成功": "Unsuccessful",
    "可敬": "Venerable",
    "有远见": "Visionary",
    "活泼": "Vivacious"
}

ResultConcept = ["Not set","Random"] + list(ConceptMap.keys())

ResultNames = [
    "照片",
    "数字艺术",
    "3D渲染",
    "绘画",
    "绘图",
    "矢量艺术"
]

ResultTypeBefore = {
    "照片": "Photo",
    "数字艺术": "Digital Artwork",
    "3D渲染": "Professional 3D rendering",
    "绘画": "Painting",
    "绘图": "Drawing",
    "矢量艺术": "Vector image"
}

#"3D渲染": ",Highly detailed,Art by senior Artist,Polycount,trending on CGSociety,trending on ArtStation",
#"Photo": ",HD,4K,8K,highly detailed,Sharp,Photo-realism,Professional photograph,Masterpiece",
    
ResultTypePositives = {
    "照片": ",Highly Detailed",
    "数字艺术": ",CGSociety,ArtStation",
    "3D渲染": ",CGSociety,ArtStation",
    "绘画": " ",
    "绘图": " ",
    "矢量艺术": ",(Flat style:1.3),Illustration,Behance"
}

ResultTypeNegatives = {
    "照片": ",Amateur,Low rated,Phone,Wedding,Frame,Painting,tumblr",
    "数字艺术": ",Scribbles,Low quality,Low rated,Mediocre,3D rendering,Screenshot,Software,UI",
    "3D渲染": ",((Wireframe)),Polygons,Screenshot,Character design,Software,UI",
    "绘画": "Low quality,Bad composition,Faded,(Photo:1.5),(Frame:1.3)",
    "绘图": ",Low quality,Photo,Artifacts,Table,Paper,Pencils,Pages,Wall",
    "矢量艺术": ",(Watermark:1.5),(Text:1.3)"
}

ResultType = {
    "Not set": "",
    "Random": "Random",
}

ResultType.update(ResultTypePositives)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

ResultDirectionList = FilesInFolder(ResourceDir + "Directions/")
ResultDirectionList = list(
    map(lambda x: x.replace(".jpg", ""), ResultDirectionList))
ResultDirection = ["Not set", "Random"] + ResultDirectionList

ResultDirectionImages = FilesInFolderFullPath(ResourceDir + "Directions/")
ResultDirectionImages = list(
    map(lambda x: x.replace("\\", "/"), ResultDirectionImages))

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

ResultMoodList = FilesInFolder(ResourceDir + "Moods/")
ResultMoodList = list(map(lambda x: x.replace(".jpg", ""), ResultMoodList))
ResultMood = ["Not set", "Random"] + ResultMoodList

ResultMoodImages = FilesInFolderFullPath(ResourceDir + "Moods/")
ResultMoodImages = list(map(lambda x: x.replace("\\", "/"), ResultMoodImages))

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

ResultArtistList = FilesInFolder(ResourceDir + "Artists/")
ResultArtistList = list(map(lambda x: x.replace(".jpg", ""), ResultArtistList))
Artists = ["Not set", "Random"] + ResultArtistList

ResultArtistImages = FilesInFolderFullPath(ResourceDir + "Artists/")
ResultArtistImages = list(
    map(lambda x: x.replace("\\", "/"), ResultArtistImages))

#ResultArtistColumn = "\n".join(str(item) for item in ResultArtistList)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

ArtMovementList = FilesInFolder(ResourceDir + "Art Movements/")
ArtMovementList = list(map(lambda x: x.replace(".jpg", ""), ArtMovementList))
ArtMovements = ["Not set", "Random"] + ArtMovementList

ArtMovementImages = FilesInFolderFullPath(ResourceDir + "Art Movements/")
ArtMovementImages = list(
    map(lambda x: x.replace("\\", "/"), ArtMovementImages))

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

ResultColorList = FilesInFolder(ResourceDir + "Colors/")
ResultColorList = list(map(lambda x: x.replace(".jpg", ""), ResultColorList))
ResultColor = ["Not set", "Random"] + ResultColorList

ResultColorImages = FilesInFolderFullPath(ResourceDir + "Colors/")
ResultColorImages = list(
    map(lambda x: x.replace("\\", "/"), ResultColorImages))

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

with open(ResourceDir + "Inspiration/Subjects.txt", 'r+') as tf:
    Subjects = [line.rstrip() for line in tf]

with open(ResourceDir + "Inspiration/Actions.txt", 'r+') as tf:
    Actions = [line.rstrip() for line in tf]

with open(ResourceDir + "Inspiration/Locations.txt", 'r+') as tf:
    Locations = [line.rstrip() for line in tf]

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

TipsAndTricks = [
    "Be specific. Add details in sequence, separated by commas. Like 'Cute black kitten, yellow eyes' + selecting Photography as image type, will get you to the result you want faster than just 'black kitten'.",
    "Try out random values. For example, set artist to random, crank up the batch count and enjoy the show. Mix and match random settings.",
    "If you add your own artist, I would recommend having 'by Artist' in front of their name. Depending on their popularity (or lack thereof) this appears to have a very tangible influence on the result.",
    "Mix and match artists from the dropdowns (or type your own) for some interesting results. Having one artist selected and other(s) set to random is also a nice way to find new looks with some amount of predictability.",
    "Parenthesis can be added to make parts of the prompt stronger. So ((cute kitten)) will make it extra cute (try it out). This is also important if a style is affecting your original prompt too much. Make that prompt stronger by adding parenthesis around it, like this: ((promt)). A strength modifier value can also be used, like this (prompt:1.1).",
    "Prompts can be split like [A|B] to sequentially use terms, one after another on each step. For example **[cat|dog]** will produce a hybrid catdog.",
    "Using **[A:B:0.4]** will switch to other terms after the first one has been active for a certain percentage of steps. So [cat:dog:0.4] will build a cat 40% of the time and then start turning it into a dog. Usually this needs more steps to work properly.",
    "During long cold winter nights, you can turn your PC into a heater by generating hundreds of images non-stop.",
    "Feel free to share feedback and ideas on github: https://github.com/some9000/StylePile",
    "Some things work together, others don't. Like Photo doesn't work too great with many Art movements or Drawing will not become photorealistic just because that was selected."
]

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

Preset = {
    "None": "",
    "肖像": ",(close portrait:1.3),thematic background",
    "女性肖像": ",(close portrait:1.3),(Feminine:1.4),(beautiful:1.4),(attractive:1.3),handsome,calendar pose,perfectly detailed eyes,studio lighting,thematic background",
    "男性肖像": ",(close portrait:1.3),(Masculine:1.4),attractive,handsome,calendar pose,perfectly detailed eyes,studio lighting,thematic background",
    "二次元艺术": ",close portrait,(manga:1.3),beautiful,attractive,handsome,trending on ArtStation,DeviantArt contest winner,CGSociety,ultrafine,detailed,studio lighting",
    "可怕的怪物": ",monster,ugly,surgery,evisceration,morbid,cut,open,rotten,mutilated,deformed,disfigured,malformed,missing limbs,extra limbs,bloody,slimy,goo,Richard Estes,Audrey Flack,Ralph Goings,Robert Bechtle,Tomasz Alen Kopera,H.R.Giger,Joel Boucquemont,ArtStation,DeviantArt contest winner,thematic background",
    "机器人": ",robot,((cyborg)),machine,futuristic,concept Art by senior character Artist,featured on zbrush central,trending on polycount,trending on ArtStation,CGSociety,hard surface modeling",
    "复古未来": ",((retrofuturism)),(science fiction),dystopian Art,ultrafine,detailed,future tech,by Clarence Holbrook CArter,by Ed Emshwiller,CGSociety,ArtStation contest winner,trending on ArtStation,DeviantArt contest winner,Fallout",
    "宣传": ",propaganda poster,soviet poster,sovietwave",
    "风景": ",naturalism,land Art,regionalism,shutterstock contest winner,trending on unsplash,featured on Flickr"
}

PresetNegatives = {
    "None": "",
    "肖像": ",robot eyes,distorted pupils,distorted eyes,Unnatural anatomy,strange anatomy,things on face",
    "女性肖像": ",robot eyes,distorted pupils,distorted eyes,Unnatural anatomy,strange anatomy,things on face",
    "男性肖像": ",robot eyes,distorted pupils,distorted eyes,Unnatural anatomy,strange anatomy,things on face",
    "二次元": ",things on face,Unnatural anatomy,strange anatomy",
    "可怕的怪物": ",(attractive),pretty,smooth,cArtoon,pixar,human",
    "机器人": ",cartoon",
    "复古未来": ",extra limbs,malformed limbs,modern",
    "宣传": ",extra limbs,malformed limbs,modern",
    "风景": ",((hdr)),((terragen)),((rendering)),(high contrast)"
}

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

# At some point in time it looked like adding a bunch of these negative prompts helps,but now I am not so sure...
AlwaysBad = ",watermark,signature"

class Script(scripts.Script):
    txt2img_prompt = None
    img2img_prompt = None
    batch_count = None
    batch_size = None
    steps = None

    def after_component(self, component, **kwargs):
        if kwargs.get('elem_id') == 'txt2img_prompt':
            self.txt2img_prompt = component
        if kwargs.get('elem_id') == 'img2img_prompt':
            self.img2img_prompt = component
        # if kwargs.get('elem_id') == 'batch_count':
        #     self.batch_count = component
        # if kwargs.get('elem_id') == 'batch_size':
        #     self.batch_size = component
        # if kwargs.get('elem_id') == 'steps':
        #     self.steps = component

    def title(self):
        return "StylePile"

    def show(self, is_img2img):
        return True

    def ui(self, is_img2img):
        with gr.Tab("Parameters"):
            with gr.Row():
                ddResultConcept = gr.Dropdown(
                    ResultConcept, label="概念", value="Not set")
                ddCoreResultType = gr.Dropdown(
                    list(ResultType.keys()), label="图片类型", value="Not set")   
                slResultTypeStrength = gr.Slider(
                    0, 2, value=1.3, step=0.05, show_label=False)
            with gr.Row():
                with gr.Column():
                    ddResultDirection = gr.Dropdown(
                        ResultDirection, label="Direction", value="Not set")
                    slResultDirectionStrength = gr.Slider(
                        0, 2, value=1.3, step=0.05, show_label=False)
                with gr.Column():
                    ddResultMood = gr.Dropdown(
                        ResultMood, label="Mood", value="Not set")
                    slResultMoodStrength = gr.Slider(
                        0, 2, value=1.3, step=0.05, show_label=False)
                with gr.Column():
                    ddResultColor = gr.Dropdown(
                        ResultColor, label="Colors", value="Not set")
                    slResultColorStrength = gr.Slider(
                        0, 2, value=1.3, step=0.05, show_label=False)
            with gr.Row():
                cbChangeCount = gr.Checkbox(
                    value=True, label="Set batch count to prompt count")
                cbIncreaseSeed = gr.Checkbox(
                    value=True, label="Increase seed with batch size")
                cbShowTips = gr.Checkbox(
                    value=False, label="Show tips when generating")
                ddPreset = gr.Dropdown(list(Preset.keys()), label="Style influence (incomplete)", value="None")
            with gr.Row():
                strSequentialPrompt = gr.Textbox(
                    lines=3, label="顺序提示 [X]", placeholder="Insert [X] anywhere in main prompt to sequentially insert values from here. Random values will be added here or to main prompt. 在主提示中的任意位置插入 [X] 以从此处顺序插入值。 随机值将添加到此处或主提示。")
            with gr.Row():
                strSubSequentialPrompt = gr.Textbox(
                    lines=3, label="SubSequential prompts [Y]", placeholder="Insert [Y] in the final prompt <== to sequentially insert values from here (and increase prompt count). This is done after all other prompts and loops through all lines. 在最后的提示<==中插入[Y]，从这里开始依次插入数值（并增加提示计数）。这是在所有其他提示之后进行的，并在所有行中循环。")

            with gr.Row():
                strRandomPromptA = gr.Textbox(
                    lines=3, label="Random [A]", placeholder="Insert [A] anywhere in main prompt (or [X] prompt) to randomly insert values from here.在主提示符（或[X]提示符）的任何地方插入[A]，从这里随机插入数值。")
                strRandomPromptB = gr.Textbox(
                    lines=3, label="Random [B]", placeholder="Insert [B] anywhere in main prompt (or [X] prompt) to randomly insert values from here.")
                strRandomPromptC = gr.Textbox(
                    lines=3, label="Random [C]", placeholder="Insert [C] anywhere in main prompt (or [X] prompt) to randomly insert values from here.")

            with gr.Row():
                with gr.Column():
                    selArtistA = gr.Dropdown(Artists, label="Artist", value="Not set")
                    sliImageArtistStrengthA = gr.Slider(0, 2, value=1.3, step=0.05, label="Influence")
                    selArtistB = gr.Dropdown(Artists, label="Artist", value="Not set")
                    sliImageArtistStrengthB = gr.Slider(0, 2, value=1.3, step=0.05, label="Influence")
                    selArtistC = gr.Dropdown(Artists, label="Artist", value="Not set")
                    sliImageArtistStrengthC = gr.Slider(0, 2, value=1.3, step=0.05, label="Influence")
                with gr.Column():
                    selArtMovementA = gr.Dropdown(ArtMovements, label="Art movement", value="Not set")
                    selArtMovementStrengthA = gr.Slider(0, 2, value=1.3, step=0.05, label="Influence")
                    selArtMovementB = gr.Dropdown(ArtMovements, label="Art movement", value="Not set")
                    selArtMovementStrengthB = gr.Slider(0, 2, value=1.3, step=0.05, label="Influence")
                    selArtMovementC = gr.Dropdown(ArtMovements, label="Art movement", value="Not set")
                    selArtMovementStrengthC = gr.Slider(0, 2, value=1.3, step=0.05, label="Influence")
            
            if self.txt2img_prompt is not None:
                with gr.Row():
                    bTestPrompt = gr.Button('Insert default prompt')
                    #if self.txt2img_prompt is not None:
                    bTestPrompt.click(fn=lambda x: "Portrait of an attractive young lady,flower field background, square ratio", 
                        inputs  = [self.txt2img_prompt],
                        outputs = [self.txt2img_prompt])
                            
                    bInspireMe = gr.Button('Inspire me, StylePile')
                    #if self.txt2img_prompt is not None:
                    bInspireMe.click(fn=lambda x: random.choice(Subjects) +","+ random.choice(Actions) +","+ random.choice(Locations)+",", 
                        inputs  = [self.txt2img_prompt],
                        outputs = [self.txt2img_prompt])

            
            # with gr.Row():
            #     b4images = gr.Button('4 images')
            #     b8images = gr.Button('8 images')
            #     b4x4images = gr.Button('4x4 images')
            #     bMorphImages = gr.Button('4@40 images')
            #     bStandardPreview = gr.Button('Preview')

            # b4images.click(fn = lambda p:40, inputs = [self.steps],outputs = [self.steps])
            # b8images.click(fn = lambda p:8, inputs = [self.batch_count],outputs = [self.batch_count])
            # b8images.click(fn = lambda p:8, inputs = [self.batch_size],outputs = [self.batch_size])

        with gr.Tab("Directions") as StyleTab:
            gr.Gallery(value=ResultDirectionImages, show_label=False).style(
                grid=(3, 3, 3, 3, 4, 4), container=False)

        with gr.Tab("Moods"):
            gr.Gallery(value=ResultMoodImages, show_label=False).style(
                grid=(3, 3, 3, 3, 4, 4), container=False)

        with gr.Tab("Artists"):
            gr.Gallery(value=ResultArtistImages, show_label=False).style(
                grid=(2, 2, 2, 2, 3, 3), container=False)
            
        with gr.Tab("Art movements"):
            gr.Gallery(value=ArtMovementImages, show_label=False).style(
                grid=(3, 3, 3, 3, 4, 4), container=False)
            
        with gr.Tab("Colors"):
            gr.Gallery(value=ResultColorImages, show_label=False).style(
                grid=(3, 3, 3, 3, 4, 4), container=False)

        with gr.Tab("Tools & Info") as HelpTab:
            with gr.Row():
                gr.Markdown(
                    """
                    ### Tips and tricks
                    If you add your own Artist, I would recommend having **by Artist** in front of their name. Depending on their popularity (or lack thereof) this appears to have a very tangible influence on the result. In general, most of the elements that influence the look appear to work best with a certain strength boost, hence the 1.3 default values.
                    Another thing to keep in mind is relationships between keywords and type of content. For example, if you want a reasonably realistic looking image of an alien cyborg. Selecting **Photo** will mostly produce fairly clumsy results. But, if you select **3D rendering** and **Realistic, Ultrarealistic** or **Ultra detailed** as direction, the result may actually be closer to what you expect. The opposite is true as well. There are certain things that you will not get to look realistic no matter what the modifiers are if Image type is not set to **Photo**. Try kittens.
                    In general just experiment with **Image type** and **Direction**. An easy way to do it is selecting random settings, a high batch count and then checking the keywords on the results you like.
                    ### Modifiers
                    Elements of the prompt can be modified to have a certain strength or change over time. Normally you do this by typing into the prompt, but here I have added tools that will actually insert pre-formatted text so it is easier to understand what it should look like. Note that it doesn't have to be a single word, it is a part of the prompt, so it can be several words or a full sentence. Also note that it will be added to the end of the prompt no matter where the cursor was due to limitations of gradio.
                    """
                    )
            with gr.Row():
                with gr.Column():
                    gr.Markdown(
                        """
                        A strength modifier value can be added to parts of the prompt like this **(A:1.3)** < this part would be about 30% stronger. To save some typing you can select the line you want to make stronger and use **Ctrl+Shift+Arrow keys up** or **down** to add these parenthesis and change the value. 1.3 seems like a good starting point if you want to see some impact. Interestingly, adding **very** as a keyword may have a similar or even stronger effect.
                        """
                    )
                with gr.Column():
                    tbAdjustStrength = gr.Textbox(label="Adjust strength", placeholder="Enter prompt here")
                    sbAdjustStrength = gr.Slider(0.1, 2.0, value=1.3, step=0.1, label="Strength") 
                    bAdjustStrength = gr.Button('Insert')
            with gr.Row():
                with gr.Column():
                    tbMorphFrom = gr.Textbox(label="Morph from", placeholder="Prompt A")
                    tbMorphTo = gr.Textbox(label="Morph to", placeholder="Prompt B")
                    sbMorphStrength = gr.Slider(0.05, 0.95, value=0.5, step=0.05, label="Starting point")    
                    bInsertMorph = gr.Button('Insert')
                with gr.Column():
                    gr.Markdown(
                        """
                        You can start with a prompt element and then, after a certain percentage of steps, start converting this prompt into something else. Basically it looks like [A:B:0.5] with A being the first part to do, B being what it should be morphing into and 0.5 representing a percentage of when it should start the conversion process. Thus in case of 0.5 that is 50% of the whole process.
                        """)
            with gr.Row():
                with gr.Column():  
                    gr.Markdown(
                        """
                        You can mix two prompt elements where each step they get swapped. It looks like [A|B] thus processing A each odd step and B each even step.
                        """)
                with gr.Column():
                    tbBounceFrom = gr.Textbox(label="Bounce from", placeholder="Prompt A")
                    rbBounceTo = gr.Textbox(label="Bounce to", placeholder="Prompt B")  
                    bBounce = gr.Button('Insert')
            with gr.Row():
                gr.Markdown(
                    """
                    These last two sections appear to benefit from increasing sampling steps and CFG scale.
                    ### Example images, adding your own selections to dropdowns
                    Example images stored in the script folders are more than just images. Their filenames are used to create the **Direction**, **Mood**, **Artist** and Art **movement** dropdown selections. This gives you the ability to Add/Remove parameters as you wish. Just place an image in the folder and name it as the option you want to see in the dropdown. Delete image file to remove that option.
                    
                    In case you would like to suggest an artist be added to the roster, I would recommend making 8+ sample images first. To see if SD actually "knows" that artist and their style appears unique enough. The portraits you can see in the info pages were generated with the following settings:
                    
                    ### Sample portrait prompt
                    Positive: Portrait of an attractive young lady,flower field background,(by [X]:1.3), square ratio
                    Negative - missing limbs, extra limbs, watermark,label,text

                    [X] is **Artist Name Surname** From my research adding **Artist** can really help to get the correct look.

                    20 steps on Euler A
                    Seed - 669 - batch of 4 images

                    Generally that produces a fairly nice portrait with enough room to show off the given style. Do compare the results to the actual style. As SD will produce something it 'thinks' may be correct based on their name (guessing nationality, basing it on something that has mentioned a similar name etc) and that influences the results, but not in a good way.
                    """)
            
            if self.txt2img_prompt is not None:
                bAdjustStrength.click(fn=lambda p,x,y: p + "(" + x + ":" + str(y) + ")",
                    inputs  = [self.txt2img_prompt,tbAdjustStrength,sbAdjustStrength],
                    outputs = [self.txt2img_prompt])

                bInsertMorph.click(fn=lambda p,x,y,z: p + "[" + x + ":" + y + ":" + str(z) + "]",
                    inputs  = [self.txt2img_prompt,tbMorphFrom,tbMorphTo,sbMorphStrength],
                    outputs = [self.txt2img_prompt])

                bBounce.click(fn=lambda p,x,y: p + "[" + x + "|" + y + "]",
                    inputs  = [self.txt2img_prompt,tbBounceFrom,rbBounceTo],
                    outputs = [self.txt2img_prompt])
                
            if self.img2img_prompt is not None:
                bAdjustStrength.click(fn=lambda p,x,y: p + "(" + x + ":" + str(y) + ")",
                    inputs  = [self.img2img_prompt,tbAdjustStrength,sbAdjustStrength],
                    outputs = [self.img2img_prompt])

                bInsertMorph.click(fn=lambda p,x,y,z: p + "[" + x + ":" + y + ":" + str(z) + "]",
                    inputs  = [self.img2img_prompt,tbMorphFrom,tbMorphTo,sbMorphStrength],
                    outputs = [self.img2img_prompt])

                bBounce.click(fn=lambda p,x,y: p + "[" + x + "|" + y + "]",
                    inputs  = [self.img2img_prompt,tbBounceFrom,rbBounceTo],
                    outputs = [self.img2img_prompt])
                
        with gr.Tab("Help"):
            gr.Markdown(
                """
                ## Hello, StylePile here
                ### Introduction
                **StylePile** is a mix and match system for adding elements to prompts that affect the style of the result. Hence the name. By default, these elements are placed in a specific order and given strength values. Which means the result sort-of evolves. I have generated thousands of images for each main **Image type** and tweaked the keywords to attempt giving expected results most of the time. Certainly, your suggestions for improvements are very welcome.
                ### Base workflow
                You select extra settings in this script and then hit the standard orange **Generate** button to get results.
                
                For example, if you select the **Painting** image type, then almost all results will look like Paintings. Selecting **Mood** will have a certain influence on the overall look in some way (if it's something humanoid it may show emotion, but also colors and overall feel may change). Setting **Colors** will change the general tonality of the result. And setting **View** will attempt to change how the subject is viewed. Attempt, because view appears to be the least reliable keyword. These elements are placed in order of influence and supported by certain strength values. These basic settings produce very quick results close to the general look you want.
                ![]({path.join(ResourceDir,"Artists.jpg") ''})
                Moving on, adding a **Art movement** will combine with **Image type** to influence how the result generally looks. These styles are based on classic and modern Painting/Art/design movements (which I picked after hours and thousands of samples of testing) and can have a strong influence on the end result. Either it will be more realistic or artistic, or look like a comic book etc. In general, this is a really strong element for getting the look you want. Its influence can be adjusted with the slider above. Experiment with the values, keeping in mind that anything above 1.5 will start becoming a mess. In a similar way, but more focused, you can select an **Artist** and, of course, that will have a very visible effect on the result as well. Currently there are 135 artists, 55 art styles and 25 emotions available for selection and represented with preview images.

                Strength of these settings has been preset at 1.3, as that appears to be the golden ratio for getting good results. Sometimes very low settings have an interesting result as well. You can, and should, freely mix and match these settings to get different results. Classic Painting styles affected or affecting 3D look quite interesting. Photography can look cool with some of the brighter, more artistic styles etc. Sometimes raising CFG scale to 15,20 or more also helps to REALLY push the style onto the image.

                ### Advanced workflow
                StylePile can overtake the generation process, allowing you to generate a large amount of different results with very little extra work. There are two types of variables you can use: [X] and [R]. When you add an [X] to your prompt, it sequentially takes values from the **Sequential prompts** text area. You can have dozens of lines there and they will be processed in sequence. When you add [R] to the prompt a value from the **Random** text area will be inserted in its place. By combining these a huge variety in prompts is very easy to do.

                When using this, **Batch count** will move through the prompts and **Batch size** will set how many copies with the given prompt to make. If the seed is not random, it will increase with each batch size step. Any random elements will still be picked randomly.

                ### In conclusion
                I made this because manually changing keywords, looking up possible styles, etc was a pain. It is meant as a fun tool to explore possibilities and make learning Stable Diffusion easier. If you have some ideas or, better yet, would like to contribute in some way*, just visit https://github.com/some9000/StylePile

                *Hey, if you have a 12Gb graphics card just laying around I'm happy to take it (:


你好，我是StylePile

简介

风格加码是一个混合和匹配系统，用于向提示语添加影响结果风格的元素。因此而得名。默认情况下，这些元素被放置在一个特定的顺序中，并给出强度值。这意味着结果有点像演化出来的。我已经为每个主要的图像类型生成了数千张图像，并调整了关键词，试图在大多数情况下给出预期的结果。当然，我们非常欢迎你的改进建议。

基本工作流程

你在这个脚本中选择额外的设置，然后点击标准的橙色生成按钮来获得结果。

例如，如果你选择了绘画图像类型，那么几乎所有的结果都会看起来像绘画。选择 "心情 "会对整体外观产生一定的影响（如果是人形的东西，可能会表现出情绪，但也会改变颜色和整体感觉）。设置颜色将改变结果的总体色调。而设置 "视图 "将试图改变主体的观看方式。试图，因为视图似乎是最不可靠的关键词。这些元素按照影响的顺序排列，并由一定的强度值支持。这些基本设置会产生非常快速的结果，接近你想要的一般外观。

![]({path.join(ResourceDir, "Artists.jpg") ''})

继续，添加一个艺术动作将与图像类型相结合，影响结果的一般外观。这些风格是基于经典和现代绘画/艺术/设计运动（这是我经过数小时和数以千计的测试样本挑选出来的），并能对最终结果产生强烈的影响。要么会更现实，要么会更艺术，要么看起来像漫画书等等。一般来说，这是一个非常强大的元素，可以获得你想要的外观。它的影响可以通过上面的滑块来调整。实验一下数值，记住，任何超过1.5的数值都会开始变得混乱。以类似的方式，但更集中，你可以选择一个艺术家，当然，这对结果也会有非常明显的影响。目前，有135位艺术家、55种艺术风格和25种情感可供选择，并有预览图片表示。

这些设置的强度被预设为1.3，因为这似乎是获得良好结果的黄金比例。有时，非常低的设置也有一个有趣的结果。你可以，而且应该自由地混合和匹配这些设置，以获得不同的结果。受影响或影响3D的经典绘画风格看起来相当有趣。摄影可以用一些更明亮、更艺术的风格等看起来很酷。有时将CFG比例提高到15、20或更高，也有助于将风格真正推到图像上。

先进的工作流程

StylePile可以超越生成过程，允许你用很少的额外工作来生成大量的不同结果。有两种类型的变量你可以使用： [X]和[R]。当你给你的提示符添加一个[X]时，它就会按顺序从顺序提示符文本区取值。你可以在那里有几十行，它们将按顺序被处理。当你在提示中添加[R]时，将从随机文本区中插入一个值来代替。通过这些组合，可以很容易地实现大量的提示信息。

使用这个方法时，生成批次将在提示中移动，每批数量将设置有多少份给定的提示。如果种子不是随机的，它将随着每批数量的增加而增加。任何随机元素仍将被随机抽取。

综上所述

我做这个是因为手动改变关键词、查找可能的样式等是一件很痛苦的事。它是作为一个有趣的工具来探索各种可能性，使学习稳定扩散更容易。如果你有一些想法，或者更好的是，想以某种方式做出贡献*，就请访问https://github.com/some9000/StylePile。

*嘿，如果你有一块12Gb的显卡，我很乐意接受它（：

            """)

        return [ddResultConcept,
                cbChangeCount,
                cbIncreaseSeed,
                strSequentialPrompt,
                strSubSequentialPrompt,
                strRandomPromptA,
                strRandomPromptB,
                strRandomPromptC,
                slResultTypeStrength,
                ddCoreResultType,
                ddResultDirection,
                slResultDirectionStrength,
                ddResultMood,
                slResultMoodStrength,
                ddResultColor,
                slResultColorStrength,
                selArtMovementStrengthA,
                selArtMovementA,
                selArtMovementStrengthB,
                selArtMovementB,
                selArtMovementStrengthC,
                selArtMovementC,
                sliImageArtistStrengthA,
                selArtistA,
                sliImageArtistStrengthB,
                selArtistB,
                sliImageArtistStrengthC,
                selArtistC,
                cbShowTips,
                ddPreset
                ]

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

    def run(self, p,
            ddResultConcept,
            cbChangeCount,
            cbIncreaseSeed,
            strSequentialPrompt: str,
            strSubSequentialPrompt: str,
            strRandomPromptA: str,
            strRandomPromptB: str,
            strRandomPromptC: str,
            slResultTypeStrength,
            ddCoreResultType,
            ddResultDirection,
            slResultDirectionStrength,
            ddResultMood,
            slResultMoodStrength,
            ddResultColor,
            slResultColorStrength,
            selArtMovementStrengthA,
            selArtMovementA,
            selArtMovementStrengthB,
            selArtMovementB,
            selArtMovementStrengthC,
            selArtMovementC,
            sliImageArtistStrengthA,
            selArtistA,
            sliImageArtistStrengthB,
            selArtistB,
            sliImageArtistStrengthC,
            selArtistC,
            cbShowTips,
            ddPreset
            ):

        # If it's all empty just exit function.
        if len(p.prompt) == 0:
            print(
                f"\nEmpty prompt! It helps to have at least some guidance for SD. Remember to insert an [X], [A] or [B] into main prompt if you want to use variable values.")
            return

        # Batch lines present?
        BatchLines = [x.strip() for x in strSequentialPrompt.splitlines()]
        LineCount = len(BatchLines)

        SubBatchLines = [x.strip() for x in strSubSequentialPrompt.splitlines()]
        SubLineCount = len(SubBatchLines)

        TempText = ""
        SubTempText = ""

        images = []
        seeds = []
        prompts = []
        infotexts = []

        # Overtake amounts of things to generate so we can go through different variables
        MainJobCount = p.n_iter
        p.n_iter = 1

        SubIterationCount = p.batch_size
        p.batch_size = 1

        # If we have [X] variables use their amount, unless unchecked
        if cbChangeCount == True and len(strSequentialPrompt) > 0:
            MainJobCount = LineCount

        SubCycleCount = 1

        if SubLineCount > 0:
            SubCycleCount = SubLineCount

        # Any random lines present?
        RandomLinesA = [r.strip() for r in strRandomPromptA.splitlines()]
        RandomLinesB = [r.strip() for r in strRandomPromptB.splitlines()]
        RandomLinesC = [r.strip() for r in strRandomPromptC.splitlines()]

        # So the progress bar works correctly
        state.job_count = MainJobCount * SubIterationCount * SubCycleCount

        CurrentChoice = 0
        SubCurrentChoice = 0

        FinalResultDirection = ""

        for x in range(MainJobCount):
            SeedStep = 0

            AllMovements = ""
            AllArtists = ""

            # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

            # Large artist selection
            if selArtistA != "Not set":
                # If Random is selected then pick a random artist
                if selArtistA == "Random":
                    AllArtists += ",(by Artist " + random.choice(ResultArtistList) + \
                        ":" + str(sliImageArtistStrengthA) + ")"
                # otherwise use the selected value
                else:
                    AllArtists += ",(by Artist " + selArtistA + \
                        ":" + str(sliImageArtistStrengthA) + ")"

            if selArtistB != "Not set":
                if selArtistB == "Random":
                    AllArtists += ",(by Artist " + random.choice(ResultArtistList) + \
                        ":" + str(sliImageArtistStrengthB) + ")"
                else:
                    AllArtists += ",(by Artist " + selArtistB + \
                        ":" + str(sliImageArtistStrengthB) + ")"

            if selArtistC != "Not set":
                if selArtistC == "Random":
                    AllArtists += ",(by Artist " + random.choice(ResultArtistList) + \
                        ":" + str(sliImageArtistStrengthC) + ")"
                else:
                    AllArtists += ",(by Artist " + selArtistC + \
                        ":" + str(sliImageArtistStrengthC) + ")"

            # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

            # Large style selection
            if selArtMovementA != "Not set":
                if selArtMovementA == "Random":
                    AllMovements += ",(" + random.choice(ArtMovementList) + ":" + str(selArtMovementStrengthA) + ")"
                else:
                    AllMovements += ",(" + selArtMovementA + ":" + str(selArtMovementStrengthA) + ")"

            if selArtMovementB != "Not set":
                if selArtMovementB == "Random":
                    AllMovements += ",(" + random.choice(ArtMovementList) + ":" + str(selArtMovementStrengthB) + ")"
                else:
                    AllMovements += ",(" + selArtMovementB + ":" + str(selArtMovementStrengthB) + ")"

            if selArtMovementC != "Not set":
                if selArtMovementC == "Random":
                    AllMovements += ",(" + random.choice(ArtMovementList) + ":" + str(selArtMovementStrengthC) + ")"
                else:
                    AllMovements += ",(" + selArtMovementC + ":" + str(selArtMovementStrengthC) + ")"

            # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

            for y in range(SubIterationCount):

                # Clear the variables so random selection can work
                FinalResultMood = ""
                FinalResultColor = ""
                FinalConcept = ""

                # Preset the selection variables
                MainType = ""

                TypeFront = ""
                TypePositives = ""
                TypeNegatives = ""

                # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                if ddResultConcept != "Not set":
                    if ddResultConcept == "Random":  
                        FinalConcept = random.choice(ElementConcept)
                    else:
                        FinalConcept = ConceptMap.get(ddResultConcept)
                else:
                    FinalConcept = ""

                # If main prompt isn't empty...
                if ResultType[ddCoreResultType] != "":
                # If it is random, give it a random value
                    if ResultType[ddCoreResultType] == "Random":
                        MainType = random.choice(ResultNames)
                    # otherwise use the selected value
                    else:
                        MainType = ddCoreResultType

                # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                if ddResultDirection != "Not set":
                    if ddResultDirection == "Random":
                        FinalResultDirection = " (" + random.choice(
                            ResultDirectionList) + ":" + str(slResultDirectionStrength) + ") "
                    else:
                        FinalResultDirection = " (" + ddResultDirection + \
                            ":" + str(slResultDirectionStrength) + ") "

                # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                # Pick the mood
                if ddResultMood != "Not set":
                    if ddResultMood == "Random":
                        FinalResultMood = ",(" + random.choice(ResultMoodList) + \
                            ":" + str(slResultMoodStrength) + ") "
                    else:
                        FinalResultMood = ",(" + ddResultMood + \
                            ":" + str(slResultMoodStrength) + ") "

                # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                # If present, add batch element, otherwise remove that reference
                TempText = ""
                if LineCount > 0:
                    if len(BatchLines[CurrentChoice % LineCount]) > 0:
                        TempText = BatchLines[CurrentChoice % LineCount]

                #TempText = copy_p.prompt.replace("[X]", TempText)
                TempText = p.prompt.replace("[X]", TempText)

                # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                # If present, add random element, otherwise remove that reference
                if len(RandomLinesA) > 0:
                    TempText = TempText.replace(
                        "[A]", random.choice(RandomLinesA))
                else:
                    TempText = TempText.replace("[A]", "")

                if len(RandomLinesB) > 0:
                    TempText = TempText.replace(
                        "[B]", random.choice(RandomLinesB))
                else:
                    TempText = TempText.replace("[B]", "")

                if len(RandomLinesC) > 0:
                    TempText = TempText.replace(
                        "[C]", random.choice(RandomLinesC))
                else:
                    TempText = TempText.replace("[C]", "")

                # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                # Colors
                if ddResultColor!= "Not set":
                    if ddResultColor == "Random":
                        FinalResultColor = ",(" + random.choice(ResultColorList) + \
                            ":" + str(slResultColorStrength) + ") "
                    else:
                        FinalResultColor = ",(" + ddResultColor + \
                            ":" + str(slResultColorStrength) + ") "

                # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                # If main prompt isn't empty...
                if MainType != "":
                    # Format our variables to merge into positive prompt...
                    TypeFront = "(" + FinalConcept + " " + ResultTypeBefore[MainType] + \
                        ":" + str(slResultTypeStrength) + ") of "
                    TypePositives = ResultTypePositives[MainType]
                    TypeNegatives = ResultTypeNegatives[MainType]

                # Our main prompt composed of all the selected elements
                MainPositive = TypeFront + FinalResultDirection + FinalResultMood + TempText + \
                    AllArtists + TypePositives + AllMovements + \
                    FinalResultColor + Preset[ddPreset]

                #MainNegative = copy_p.negative_prompt
                MainNegative = p.negative_prompt

                # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                SubCurrentChoice = 0

                for z in range(SubCycleCount):
                    # Copy of the main prompt module to make batches, I guess...
                    copy_p = copy.copy(p)

                    if copy_p.seed != -1:  # and 'p.seed' in locals():
                        copy_p.seed += SeedStep

                    SubTempText = ""
                    if SubLineCount > 0:
                        if len(SubBatchLines[SubCurrentChoice % SubLineCount]) > 0:
                            SubTempText = SubBatchLines[SubCurrentChoice % SubLineCount]

                    TempText = MainPositive.replace("[Y]", SubTempText)

                    TempText = TempText.replace("[xs]", str(random.randrange(100000,999999,1)))
                    TempText = TempText.replace("[XS]", str(random.randrange(100000,999999,1)))                    

                    TempText = TempText.replace("[s]", ''.join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5)))
                    TempText = TempText.replace("[S]", ''.join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5)))
                    
                    TempText = TempText.replace("[m]", ''.join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=10)))
                    TempText = TempText.replace("[M]", ''.join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=10)))
                    
                    TempText = TempText.replace("[l]", ''.join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5)) + " " + ''.join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5)))
                    TempText = TempText.replace("[L]", ''.join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5)) + " " + ''.join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5)))
                    
                    TempText = TempText.replace("[xl]", ''.join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=10)) + " " + ''.join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=10)))
                    TempText = TempText.replace("[XL]", ''.join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=10)) + " " + ''.join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=10)))

                    # Clean up positive prompt
                    TempText = " ".join(TempText.split())
                    TempText = TempText.replace(",,", ",")
                    TempText = TempText.replace(" ,", ",")
                    TempText = TempText.replace(",", ",")
                    TempText = TempText.replace("( ", "(")
                    TempText = TempText.replace(" )", ")")
                    TempText = TempText.strip(",")
                    TempText = TempText.strip()

                    copy_p.prompt = TempText

                    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->

                    # Clean up negative prompt
                    TempText = MainNegative + TypeNegatives + \
                        AlwaysBad + PresetNegatives[ddPreset]

                    TempText = " ".join(TempText.split())
                    TempText = " ".join(TempText.split())
                    TempText = TempText.replace(",,", ",")
                    TempText = TempText.replace(" ,", ",")
                    TempText = TempText.replace(",", ",")
                    TempText = TempText.replace("( ", "(")
                    TempText = TempText.replace(" )", ")")
                    TempText = TempText.strip(",")
                    TempText = TempText.strip()

                    copy_p.negative_prompt = TempText

                    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->
                    # Add information in command prompt window and process the image

                    print(f"\n\n[Prompt {x+1}/{MainJobCount}][Iteration {y+1}/{SubIterationCount}][SubPrompt {z}/{SubLineCount}][Seed {int(copy_p.seed)}] >>> Positives <<< {copy_p.prompt} >>> Negatives <<< {copy_p.negative_prompt}\n")

                    proc = process_images(copy_p)
                    infotexts += proc.infotexts
                    images += proc.images
                    seeds.append(proc.seed)
                    prompts.append(proc.prompt)

                    SubCurrentChoice += 1

                    if cbIncreaseSeed == True:
                        SeedStep += 1

            CurrentChoice += 1

        p.batch_size = MainJobCount
        p.n_iter = SubIterationCount

        if cbShowTips:
            print(
                f"\n\nStylePile processing complete. Here's a random tip:\n{random.choice(TipsAndTricks)}\n")

        return Processed(p=p, images_list=images, seed=p.seed, all_seeds=seeds, all_prompts=prompts, info=infotexts[0],
                         infotexts=infotexts)
