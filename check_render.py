#!/usr/bin/env python3
"""
TruthLens UA Analytics - Render Deploy Checker
Автоматична перевірка деплою на Render
"""

import requests
import time
import sys
from datetime import datetime

def check_render_deployment():
    """Перевіряє статус деплою на Render"""
    
    render_url = "https://truthlens-ua-analytics.onrender.com"
    api_url = f"{render_url}/_stcore/health"
    
    print("🚀 TruthLens UA Analytics - Render Deploy Checker")
    print("=" * 50)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 URL: {render_url}")
    print()
    
    # Перевірка основного додатку
    print("🔍 Перевірка Dashboard...")
    try:
        response = requests.get(render_url, timeout=10)
        if response.status_code == 200:
            print("✅ Dashboard: ГОТОВИЙ")
            print(f"   Статус: {response.status_code}")
            print(f"   Розмір: {len(response.content)} bytes")
        else:
            print(f"❌ Dashboard: Помилка {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Dashboard: Не доступний ({e})")
        return False
    
    print()
    
    # Перевірка API
    print("🔍 Перевірка API...")
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            print("✅ API: ГОТОВИЙ")
            print(f"   Статус: {response.status_code}")
            try:
                data = response.json()
                print(f"   Версія: {data.get('version', 'N/A')}")
                print(f"   Моделі: {'Завантажено' if data.get('models_loaded') else 'Не завантажено'}")
            except:
                print("   Ответ: HTML (можливо redirect)")
        else:
            print(f"❌ API: Помилка {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API: Не доступний ({e})")
        return False
    
    print()
    print("🎉 Перевірка завершена! Система працює коректно.")
    print(f"🌐 Доступ: {render_url}")
    print(f"📚 Docs: {render_url}/docs")
    
    return True

def wait_for_deployment(max_wait=300):
    """Чекає на завершення деплою"""
    
    render_url = "https://truthlens-ua-analytics.onrender.com"
    
    print("⏳ Чекаю на завершення деплою...")
    print(f"⏱️  Максимальний час очікування: {max_wait} секунд")
    print()
    
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(render_url, timeout=5)
            if response.status_code == 200:
                print("✅ Деплой завершено!")
                return True
        except:
            pass
        
        elapsed = int(time.time() - start_time)
        remaining = max_wait - elapsed
        print(f"⏳ Чекаю... ({elapsed}/{max_wait} секунд)")
        time.sleep(10)
    
    print("❌ Час очікування вичерпано")
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--wait":
        wait_for_deployment()
    
    check_render_deployment()
