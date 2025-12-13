# ZDB - پایگاه داده Key-Value سبک بر پایه SQLite

ZDB یک دیتابیس **Key-Value ساده و سبک** با استفاده از SQLite است.  
این کتابخانه امکاناتی مثل **ذخیره‌سازی خودکار، صف تغییرات (queue)، کش داخلی، عملیات اتمیک و پشتیبانی از مدل‌ها** را فراهم می‌کند تا ذخیره‌سازی محلی سریع و راحت باشد، بدون نیاز به دیتابیس کامل.

![icon](https://zdb.parssource.ir/icon.ico)

---

## ویژگی‌ها / Features

- رابط کاربری ساده Key-Value (`db[key] = value`)  
- پشتیبانی از انواع داده‌ها: `int`, `str`, `float`, `list`, `dict` و ساختارهای تو در تو  
- **Proxy types**: `ZValue`, `ZList`, `ZDict` برای track خودکار تغییرات و ذخیره‌سازی  
- ذخیره خودکار و **صف تغییرات** برای عملکرد بهتر  
- **کش داخلی** برای افزایش سرعت خواندن داده‌ها  
- پشتیبانی از **backup** دستی یا دوره‌ای  
- عملیات اتمیک (`increment`, `append_if_not_exists`)  
- مدیریت تراکنش‌ها (`with db.transaction():`)  
- پشتیبانی اختیاری از **Model** با type hints و multi-table  
- پشتیبانی از namespace برای چند جدول در یک دیتابیس  
- رمزگذاری اختیاری با SQLCipher  
- نسخه سینک (sync) کامل، نسخه async جداگانه

---

## نصب / Installation

نسخه سینک ZDB با کتابخانه‌های داخلی پایتون کار می‌کند:  
`sqlite3`, `json`, `threading`, `os`, `shutil` و غیره.  

```bash
pip install zdb
```