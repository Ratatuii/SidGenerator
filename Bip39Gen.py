import secrets
import os
from mnemonic import Mnemonic

# Функция для получения словаря BIP39 (если он не найден, скачивает его)
def get_bip39_wordlist():
    wordlist_filename = 'english.txt'
    if os.path.exists(wordlist_filename):
        with open(wordlist_filename, 'r') as f:
            return f.read().strip().split('\n')
    else:
        print("Dictionary not found. Downloading...")
        try:
            import requests
            response = requests.get('https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt')
            if response.status_code == 200:
                wordlist = response.text.strip().split('\n')
                with open(wordlist_filename, 'w') as f:
                    f.write(response.text)
                return wordlist
            else:
                print("Unable to fetch BIP39 wordlist.")
                return []
        except requests.RequestException as e:
            print(f"Error downloading dictionary: {e}")
            return []

# Генерация случайной энтропии для BIP39
def generate_entropy(bits=128):
    entropy = secrets.token_bytes(bits // 8)  # Создаем байты случайной энтропии
    return entropy

# Функция для преобразования энтропии в сид-фразу BIP39
def entropy_to_bip39_seed(entropy, wordlist):
    m = Mnemonic("english")
    # Получаем бинарное представление энтропии и проверяем контрольную сумму
    bip39_mnemonic = m.to_mnemonic(entropy)
    return bip39_mnemonic

# Функция для сохранения сид-фраз в файл
def save_mnemonics_to_file(filename, mnemonics, batch_size=100):
    with open(filename, 'a') as file:
        for mnemonic in mnemonics:
            file.write(f"{mnemonic}\n")
    print(f"Saved {batch_size} mnemonics to {filename}")

# Основная функция для генерации и сохранения сид-фраз
def main(total_count=1000):
    wordlist = get_bip39_wordlist()
    if wordlist:
        # Список для хранения сгенерированных сид-фраз
        mnemonics_batch = []
        
        for i in range(total_count):
            # Генерация случайной энтропии
            entropy = generate_entropy()
            # Преобразуем энтропию в сид-фразу
            mnemonic = entropy_to_bip39_seed(entropy, wordlist)
            mnemonics_batch.append(mnemonic)
        
        # Сохраняем все сид-фразы в файл сразу
        save_mnemonics_to_file('mnemonics.txt', mnemonics_batch, total_count)
    else:
        print("Не удалось загрузить словарь.")

if __name__ == "__main__":
    main(total_count=10000000)
