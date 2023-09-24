# Здесь происходят импорты необходимых модулей: hashlib для хеширования данных, json для работы с JSON-представлением,
# functools.reduce для выполнения операции свертки (reduction), и time для работы с временем.
import hashlib
import json
from functools import reduce
from time import time

class Blck:
    # Это конструктор класса Blck, который инициализирует объект блока с различными параметрами:
    # slf - ключевое слово для обращения к текущему объекту.
    # indx - индекс блока в цепи.
    # prv_hash - хэш предыдущего блока для обеспечения целостности цепи.
    # trnsctns - список транзакций, включенных в блок.
    # prf - доказательство выполнения работы (Proof of Work).
    # tstamp - метка времени создания блока (по умолчанию текущее время, если не указана).

    def __init__(slf, indx, prv_hash, trnsctns, prf, tstamp=None):
        # Доказательство выполнения работы (Proof of Work)
        slf.proof=prf
        # Хэш предыдущего блока для обеспечения целостности цепи
        slf.previous_hash=prv_hash
        # Индекс блока в цепи
        slf.index=indx
        # Список транзакций, включенных в блок
        slf.transactions=trnsctns
        # Корень Merkle Tree для хранения и верификации транзакций
        slf.merkle_root=None        
        # Метка времени создания блока (по умолчанию текущее время)
        slf.timestamp=tstamp or time()

    def hash_blck(slf):
        # Вычислить хэш блока, используя JSON-представление блока и SHA-256
        block_string=json.dumps(slf.__dict__, sort_keys=True)
        # строка JSON хэшируется с использованием алгоритма SHA-256,
        # и результат возвращается в виде шестнадцатеричной строки (hexdigest()).
        return hashlib.sha256(block_string.encode()).hexdigest()

# Эта функция полезна для конвертации блока или его атрибутов в формат, который легко сохранить или передать,
# например, для последующей сериализации в JSON или другой формат данных.
    def to_dict(slf): 
        # Представить блок в виде словаря для последующего использования
        return {
            'index':slf.index,
            'previous_hash':slf.previous_hash,
            'proof':slf.proof,
            'timestamp':slf.timestamp,
            'transactions':slf.transactions,
            'merkle_root':slf.merkle_root
        }

# Эта функция вычисляет корень Merkle Tree для списка транзакций
    def calc_merkle_root(slf):
        # Сначала проверяется, есть ли в списке хотя бы одна транзакция. Если транзакций нет, функция возвращает пустую строку.
        if 0==len(slf.transactions):
            return ""

        def merkle_tree_hash(tx_1, tx_2):
            # Функция использует внутреннюю функцию merkle_tree_hash, которая принимает два аргумента (tx_1 и tx_2), объединяет их
            # и вычисляет хеш SHA-256 для этой комбинации. Это выполняется последовательно для пар транзакций в списке.
            cnct_tx=tx_2+tx_1
            return hashlib.sha256(cnct_tx.encode()).hexdigest()

        merkle_tree=slf.transactions[:]
        # пока в списке merkle_tree есть более одного элемента, пары элементов объединяются и хешируются, создавая новый список хешей.
        # Этот процесс повторяется до тех пор, пока не останется только один хеш, который и является корнем Merkle Tree.
        while 1<len(merkle_tree): 
            merkle_tree=[merkle_tree_hash(merkle_tree[x], merkle_tree[x+1]) for x in range(0, len(merkle_tree), 2)]

        return merkle_tree[0]
