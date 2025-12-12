import requests
import re
import os
from bs4 import BeautifulSoup
import urllib.parse


def fate(constellation):
    dict_ = {"水瓶座": "aquarius",
             "双鱼座": "pisces",
             "白羊座": "aries",
             "金牛座": "taurus",
             "双子座": "gemini",
             "巨蟹座": "cancer",
             "狮子座": "leo",
             "处女座": "virgo",
             "天秤座": "libra",
             "天蝎座": "scorpio",
             "射手座": "sagittarius",
             "摩羯座": "capricorn"}

    url = "https://www.xzw.com/fortune/" + dict_[constellation] + "/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        content = response.text
    except Exception as e:
        print(f"获取数据失败: {e}")
        return get_default_data()

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(content, 'html.parser')

    # 获取详细运势数据
    fortune_data = {}
    indices = {}

    # 提取综合运势评分（星星数量）
    fortune_data['综合运势评分'] = 3  # 默认值

    try:
        # 方法1：从星星评分条提取 - 最准确的方法
        star_bar = soup.select_one('span.star_m.star_blue em')
        if star_bar:
            style_width = star_bar.get('style', '')
            width_match = re.search(r'width:\s*(\d+)px', style_width)
            if width_match:
                width_px = int(width_match.group(1))
                # 每颗星20px，总宽度100px（5星）
                stars_count = round(width_px / 20)
                if 1 <= stars_count <= 5:
                    fortune_data['综合运势评分'] = stars_count

        # 方法2：从图表数据中提取 - 备用方法
        if fortune_data['综合运势评分'] == 3:
            # 查找图表中的综合指数
            chart_data_match = re.search(
                r'"综合指数".*?data:\s*\[(.*?)\]', str(soup))
            if chart_data_match:
                data_str = chart_data_match.group(1)
                numbers = re.findall(r'(\d+(?:\.\d+)?)', data_str)
                if numbers:
                    # 取最新的综合指数
                    latest_score = float(numbers[-1])
                    # 将0-5分转换为1-5星
                    stars_count = max(1, min(5, round(latest_score)))
                    fortune_data['综合运势评分'] = stars_count

        # 方法3：从其他星星评分元素中提取
        if fortune_data['综合运势评分'] == 3:
            # 查找其他可能的星星评分
            star_elements = soup.find_all(
                class_=re.compile(r'star_m|star_rating'))
            for elem in star_elements:
                em_elem = elem.find('em')
                if em_elem and em_elem.get('style'):
                    width_match = re.search(
                        r'width:\s*(\d+)px', em_elem.get('style', ''))
                    if width_match:
                        width_px = int(width_match.group(1))
                        stars_count = round(width_px / 20)
                        if 1 <= stars_count <= 5:
                            fortune_data['综合运势评分'] = stars_count
                            break

    except Exception as e:
        print(f"提取星星评分失败: {e}")
        fortune_data['综合运势评分'] = 3

    # 提取各项指数 - 更精确的正则表达式
    text_content = soup.get_text()

    # 健康指数
    health_patterns = [
        r'健康指数[：:]\s*(\d+)%?',
        r'健康.*?\s*(\d+)%?',
        r'健康.*?指数[：:]\s*(\d+)'
    ]
    indices['健康指数'] = extract_number(text_content, health_patterns, 75)

    # 商谈指数
    discuss_patterns = [
        r'商谈指数[：:]\s*(\d+)%?',
        r'商谈.*?\s*(\d+)%?',
        r'商谈.*?指数[：:]\s*(\d+)'
    ]
    indices['商谈指数'] = extract_number(text_content, discuss_patterns, 70)

    # 幸运颜色
    # 幸运颜色 - 修复提取逻辑，避免包含"幸运数字"
    color_patterns = [
        r'幸运颜色[：:]\s*([\u4e00-\u9fa5]+?)(?:幸运数字|$)',  # 只提取颜色，到"幸运数字"为止
        r'幸运色[：:]\s*([\u4e00-\u9fa5]+?)(?:幸运数字|$)',   # 只提取颜色，到"幸运数字"为止
        r'颜色.*?幸运[：:]\s*([\u4e00-\u9fa5]+?)(?:幸运数字|$)'  # 只提取颜色，到"幸运数字"为止
    ]
    indices['幸运颜色'] = extract_text(text_content, color_patterns, '蓝色')

    # 幸运数字
    number_patterns = [
        r'幸运数字[：:]\s*(\d+)',
        r'幸运.*?数字[：:]\s*(\d+)',
        r'数字.*?幸运[：:]\s*(\d+)'
    ]
    indices['幸运数字'] = extract_number(text_content, number_patterns, 7)

    # 获取今日综合运势解读
    comprehensive_text = extract_fortune_description(soup, text_content)

    return {
        'indices': indices,
        'comprehensive_text': comprehensive_text,
        'stars': fortune_data['综合运势评分']
    }


def extract_number(text, patterns, default):
    """从文本中提取数字"""
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return int(match.group(1))
            except:
                continue
    return default


def extract_text(text, patterns, default):
    """从文本中提取文本"""
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return default


def extract_fortune_description(soup, text_content):
    """提取运势描述"""
    try:
        # 尝试多种方式提取运势描述
        description = ""

        # 方式1：查找综合运势区域
        fortune_section = soup.find('div', class_='c_cont')
        if fortune_section:
            desc_text = fortune_section.find('span')
            if desc_text:
                description = desc_text.get_text().strip()

        # 方式2：使用正则表达式
        if not description:
            patterns = [
                r'综合运势</strong><span>(.*?)</span>',
                r'整体运势[：:]?(.*?)[。！？]',
                r'今日运势[：:]?(.*?)[。！？]',
                r'今日.*?运势[：:]?(.*?)[。！？]'
            ]

            for pattern in patterns:
                match = re.search(pattern, str(soup), re.DOTALL)
                if match:
                    description = match.group(1).strip()
                    break

        # 清理HTML标签和多余空格
        if description:
            description = re.sub(r'<[^>]+>', '', description)
            description = re.sub(r'\s+', ' ', description)

            # 彻底清理所有可能的干扰信息 - 使用更通用的正则表达式
            # 匹配"星"后面跟着任意字符（包括字母、数字、特殊符号）再跟着"座"的模式
            description = re.sub(
                r'星[^\u4e00-\u9fa5]*座[^\u4e00-\u9fa5]*屋?', '', description)

            # 清理单独的"星"字后面跟着非中文字符
            description = re.sub(r'星[^\u4e00-\u9fa5\w]*', '', description)

            # 清理"座"字后面跟着非中文字符
            description = re.sub(r'座[^\u4e00-\u9fa5\w]*', '', description)

            # 清理"屋"字前面可能有的干扰字符
            description = re.sub(r'[^\u4e00-\u9fa5\w]*屋', '', description)

            # 清理残留的英文、数字、特殊字符组合
            description = re.sub(r'[a-zA-Z0-9]+$', '', description)

            description = description.strip()

            if len(description) > 10:  # 确保有有效内容
                return description

        # 方式3：从页面主要内容中提取
        if not description:
            main_content = soup.find('div', class_='main')
            if main_content:
                paragraphs = main_content.find_all('p')
                for p in paragraphs:
                    text = p.get_text().strip()
                    if len(text) > 20 and '运势' in text:
                        description = text
                        break

        return description if description else "今日运势平稳，保持积极心态，顺其自然即可。"

    except Exception as e:
        print(f"提取运势描述失败: {e}")
        return "今日运势平稳，保持积极心态，顺其自然即可。"


def get_default_data():
    """返回默认数据"""
    return {
        'indices': {
            '健康指数': 75,
            '商谈指数': 70,
            '幸运颜色': '蓝色',
            '幸运数字': 7
        },
        'comprehensive_text': "今日运势平稳，保持积极心态，顺其自然即可。",
        'stars': 3
    }


def download_image(url, save_path):
    """下载图片到本地"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, timeout=15, headers=headers)
        response.raise_for_status()

        if len(response.content) > 1024:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"下载图片失败: {url} - {e}")
        return False


def web(avatar, zodiac, trait, fortune_data):
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 修复路径分隔符问题
    avatar_relative_path = avatar.replace('\\', '/')
    if not avatar_relative_path.startswith('../'):
        avatar_relative_path = '../' + avatar_relative_path

    # 获取运势数据
    indices = fortune_data.get('indices', {})
    comprehensive_text = fortune_data.get('comprehensive_text', trait)
    stars = fortune_data.get('stars', 3)

    # 生成星星图标
    star_icons = '⭐' * stars + '☆' * (5 - stars)

    # 完整的HTML页面
    html_code = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>今日运势 - {zodiac}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            font-family: 'Arial', sans-serif;
        }}
        
        .fortune-container {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            color: white;
        }}
        
        .zodiac-header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .zodiac-avatar {{
            width: 100px;
            height: 100px;
            border-radius: 50%;
            margin: 0 auto 20px;
            background: rgba(255, 255, 255, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            border: 3px solid rgba(255, 255, 255, 0.3);
        }}
        
        .zodiac-avatar img {{
            width: 80px;
            height: 80px;
            border-radius: 50%;
        }}
        
        .stars-display {{
            text-align: center;
            margin-bottom: 25px;
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
        }}
        
        .stars {{
            font-size: 28px;
            margin: 10px 0;
            letter-spacing: 2px;
        }}
        
        .score {{
            font-size: 20px;
            font-weight: bold;
            color: #ffd700;
            margin-top: 5px;
        }}
        
        .indices-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 25px;
        }}
        
        .index-item {{
            background: rgba(255, 255, 255, 0.15);
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
        }}
        
        .index-item:hover {{
            transform: translateY(-2px);
            background: rgba(255, 255, 255, 0.2);
        }}
        
        .label {{
            display: block;
            font-size: 14px;
            margin-bottom: 8px;
            opacity: 0.8;
            font-weight: 500;
        }}
        
        .value {{
            font-size: 18px;
            font-weight: bold;
            color: #fff;
        }}
        
        .color-badge {{
            padding: 4px 12px;
            border-radius: 20px;
            color: white;
            font-size: 14px;
            display: inline-block;
        }}
        
        .comprehensive-section {{
            background: rgba(255, 255, 255, 0.15);
            padding: 25px;
            border-radius: 15px;
            margin-top: 20px;
            border-left: 4px solid #ffd700;
        }}
        
        .comprehensive-section h3 {{
            color: #ffd700;
            font-size: 20px;
            margin-bottom: 15px;
            font-weight: bold;
        }}
        
        .comprehensive-text {{
            font-size: 16px;
            line-height: 1.8;
            text-align: justify;
            opacity: 0.95;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 30px;
            font-size: 14px;
            opacity: 0.7;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="fortune-container">
        <div class="zodiac-header">
            <div class="zodiac-avatar">
                <img src="{avatar_relative_path}" alt="{zodiac}">
            </div>
            <h1 style="font-size: 32px; margin-bottom: 10px;">{zodiac}</h1>
            <p style="font-size: 18px; opacity: 0.8;">{trait}</p>
        </div>
        
        <div class="stars-display">
            <h3 style="font-size: 22px; margin-bottom: 10px;">✨ 今日综合运势 ✨</h3>
            <div class="stars">{star_icons}</div>
            <div class="score">{stars}/5 星</div>
        </div>
        
        <div class="indices-grid">
            <div class="index-item">
                <span class="label">💗 健康指数</span>
                <span class="value">{indices.get('健康指数', 75)}%</span>
            </div>
            <div class="index-item">
                <span class="label">💬 商谈指数</span>
                <span class="value">{indices.get('商谈指数', 70)}%</span>
            </div>
            <div class="index-item">
                <span class="label">🎨 幸运颜色</span>
                <span class="value">
                    <span class="color-badge" style="background-color: {indices.get('幸运颜色', '蓝色')}">
                        {indices.get('幸运颜色', '蓝色')}
                    </span>
                </span>
            </div>
            <div class="index-item">
                <span class="label">🔢 幸运数字</span>
                <span class="value">{indices.get('幸运数字', 7)}</span>
            </div>
        </div>
        
        <div class="comprehensive-section">
            <h3>📊 今日综合运势解读</h3>
            <div class="comprehensive-text">
                {comprehensive_text}
            </div>
        </div>
        
        <div class="footer">
            ✨ 星座运势仅供参考，保持积极心态最重要 ✨
        </div>
    </div>
</body>
</html>"""

    output_path = os.path.join(output_dir, f"{zodiac}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_code)

    print(f"✅ 已生成网页: {output_path}")

    try:
        os.startfile(output_path)
    except:
        try:
            os.system(f"start {output_path}")
        except:
            print(f"请手动打开: {output_path}")

# 向后兼容的原始函数


def fate_old(constellation):
    dict_ = {"水瓶座": "aquarius",
             "双鱼座": "pisces",
             "白羊座": "aries",
             "金牛座": "taurus",
             "双子座": "gemini",
             "巨蟹座": "cancer",
             "狮子座": "leo",
             "处女座": "virgo",
             "天秤座": "libra",
             "天蝎座": "scorpio",
             "射手座": "sagittarius",
             "摩羯座": "capricorn"}

    url = "https://www.xzw.com/fortune/" + dict_[constellation] + "/"
    response = requests.get(url)
    response.encoding = 'utf-8'
    content = response.text

    try:
        detail_comprehensive = re.findall(
            '综合运势</strong><span>(.*?)</span>', content)[0]
    except:
        detail_comprehensive = "暂无数据"
    return detail_comprehensive
