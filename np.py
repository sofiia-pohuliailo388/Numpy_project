import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns
from astroquery.jplhorizons import Horizons
from datetime import datetime, timedelta

def get_body_data(name, start_date, epochs=200, step='3d'):
    """
    Отримує вектори стану (позицію та швидкість) для будь-якого космічного тіла.
    Виправляє проблему неоднозначності назв (Ambiguous target name).
    """
    # Словник для автоматичного перетворення назв у однозначні ID барицентрів
    shortcuts = {
        'mercury': '1', 'venus': '2', 'earth': '3', 
        'mars': '4', 'jupiter': '5', 'saturn': '6', 
        'uranus': '7', 'neptune': '8', 'pluto': '9',
        'moon': '301', 'ceres': '1', 'vesta': '4'
    }
    
    clean_name = name.lower().strip()
    target_id = shortcuts.get(clean_name, name)
    
    # Розрахунок кінцевої дати для запиту
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    days_to_add = epochs * int(''.join(filter(str.isdigit, step)))
    stop_date = (start_dt + timedelta(days=days_to_add)).strftime('%Y-%m-%d')
    
    try:
        # Запит векторів: координати відносно Сонця (@sun)
        obj_query = Horizons(id=target_id, location='@sun', 
                             epochs={'start': start_date, 'stop': stop_date, 'step': step})
        obj = obj_query.vectors()
        
        # Константи для переведення (AU -> км, AU/day -> км/с)
        au_to_km = 149597870.7
        
        x = obj['x'] * au_to_km
        y = obj['y'] * au_to_km
        z = obj['z'] * au_to_km
        
        # Обчислення швидкості в км/с
        vx = obj['vx'] * au_to_km / 86400
        vy = obj['vy'] * au_to_km / 86400
        vz = obj['vz'] * au_to_km / 86400
        v = np.sqrt(vx**2 + vy**2 + vz**2)
        
        return {
            'name': name.capitalize(),
            'x': x, 'y': y, 'z': z,
            'v': v
        }
    except Exception as e:
        print(f"\n[!] Помилка пошуку '{name}': {e}")
        return None

def run_solar_system_sim():
    print("--- Симулятор орбіт на базі NASA JPL Horizons ---")
    print("Введіть назви (напр.: Earth, Mars, Jupiter, 1P/Halley, Ceres)")
    user_input = input("Список тіл через кому: ")
    names = [n.strip() for n in user_input.split(',')]
    
    start_date = datetime.now().strftime('%Y-%m-%d')
    bodies_data = []
    
    print("Завантаження даних з NASA...")
    for name in names:
        data = get_body_data(name, start_date)
        if data:
            bodies_data.append(data)
    
    if not bodies_data:
        print("Не вдалося завантажити жодного об'єкта. Перевірте назви.")
        return

    # Налаштування візуалізації
    sns.set_theme(style="dark")
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
    ax.set_facecolor('black')
    
    # Малюємо Сонце
    ax.scatter(0, 0, color='gold', s=300, label='Sun', zorder=10, 
               edgecolors='orange', linewidth=2)
    
    lines = []
    points = []
    texts = []
    colors = plt.cm.plasma(np.linspace(0.2, 0.9, len(bodies_data)))

    for i, body in enumerate(bodies_data):
        color = colors[i]
        # Пунктирна лінія всієї орбіти
        ax.plot(body['x'], body['y'], color=color, alpha=0.2, linestyle=':', linewidth=1)
        
        # Об'єкти анімації
        line, = ax.plot([], [], color=color, linewidth=2, alpha=0.8) # Хвіст
        point, = ax.plot([], [], 'o', color=color, markersize=10, markeredgecolor='white')
        text = ax.text(0, 0, '', color='white', fontsize=10, fontweight='bold')
        
        lines.append(line)
        points.append(point)
        texts.append(text)

    # Визначення масштабу (щоб бачити всі об'єкти)
    all_x = np.concatenate([b['x'] for b in bodies_data])
    all_y = np.concatenate([b['y'] for b in bodies_data])
    limit = max(np.max(np.abs(all_x)), np.max(np.abs(all_y))) * 1.1
    
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_aspect('equal')
    ax.axis('off')

    def animate(frame):
        updated_elements = []
        for i, body in enumerate(bodies_data):
            # Поточна позиція
            px, py = body['x'][frame], body['y'][frame]
            
            # Оновлення точки та тексту
            points[i].set_data([px], [py])
            texts[i].set_position((px, py))
            texts[i].set_text(f" {body['name']}\n {body['v'][frame]:.2f} km/s")
            
            # Оновлення хвоста (останні 15 кроків)
            start_tail = max(0, frame - 15)
            lines[i].set_data(body['x'][start_tail:frame+1], body['y'][start_tail:frame+1])
            
            updated_elements.extend([points[i], lines[i], texts[i]])
        return updated_elements

    # Створення анімації
    num_frames = len(bodies_data[0]['x'])
    ani = FuncAnimation(fig, animate, frames=num_frames, interval=40, blit=True, repeat=True)
    
    plt.title(f"Simulation Start: {start_date} (NASA JPL Data)", color='white', pad=20, fontsize=15)
    plt.legend(loc='upper right', facecolor='#111', labelcolor='white', framealpha=0.5)
    
    print("Відображення графіку...")
    plt.show()

if __name__ == "__main__":
    run_solar_system_sim()