import whois
from datetime import datetime

def get_creation_date(url3):
    try:
        # 使用 whois來查詢
        domain_info = whois.whois(url3)

        # 獲得 Creation Date
        creation_date = domain_info.creation_date

        # 如果 creation_date 是列表，则使用列表中的第一个日期
        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        return creation_date
    except Exception as e:
        print(f"Failed to retrieve Creation Date: {e}")
        return None

def calculate_time_difference(creation_date):
    try:
        # 取當下日期和時間
        current_datetime = datetime.now()

        # 計算當下時間-伺服器時間
        time_difference = current_datetime - creation_date

        # 取得天數、忽略HR、min和秒數
        days_difference = time_difference.days

        return days_difference
    except Exception as e:
        print(f"Failed to calculate time difference: {e}")
        return None

#if __name__ == "__main__":
    # 用户输入网址
#    url3 = input("請輸入網址: ")

    # 获取 Creation Date
#    creation_date = get_creation_date(url3)

#   if creation_date:
#        print(f"Creation Date: {creation_date}")

        # 只提取天數，計算和伺服器日期的時間差（只提取天数）
#        days_difference = calculate_time_difference(creation_date)

#        if days_difference is not None:
#            print(f"此伺服器建立至今已成立: {days_difference} days")
#        else:
#            print("Failed to calculate time difference.")
#    else:
#        print("Failed to retrieve Creation Date.")
