import hashlib
from blck import Blck

class Blckchain:
    def __init__(slf):
        slf.chain=[] #  пустой список для хранения блоков в цепочке
        slf.current_transactions=[] #  пустой список для хранения текущих транзакций
        # Genesis block
        slf.create_block(proof=100, previous_hash='1') # 1-ый дефолтный блок

    def create_block(self, proof, previous_hash=None):
        block = Blck(len(self.chain) + 1, previous_hash or self.hash(
            self.chain[-1]), self.current_transactions, proof)
        # Reset the list of transactions
        self.current_transactions=[]
        self.chain.append(block)
        return block

    @staticmethod
    # Mетод принимает блок и вызывает метод hash_blck() на этом блоке, возвращая его хеш.
    def hash(block):
        return block.hash_blck()

# Метод добавляет новую транзакцию в список текущих транзакций. Транзакции представлены в виде
# словаря с отправителем, получателем и суммой.
    def add_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender':sender,
            'recipient':recipient,
            'amount':amount,
        })

# Метод проверяет целостность блокчейна. Он проверяет хеш каждого блока, чтобы убедиться,
# что он корректно связан с предыдущим блоком, и также проверяет доказательство выполнения работы
# (Proof of Work) для каждого блока.
    def is_chain_valid(self):
        for y in range(1, len(self.chain)): # Этот цикл выполняется для каждого блока в цепочке, начиная со второго блока (индекс 1) и до последнего блока.
            current_block=self.chain[y]
            previous_block=self.chain[y-1]

            # Эта строка проверяет, является ли хеш текущего блока (current_block) корректным.
            # Он сравнивается с хешем предыдущего блока (previous_block), который должен быть указан в текущем блоке.
            # Если хеши не совпадают, это может означать, что цепочка была повреждена или изменена, и
            # метод возвращает False, указывая на недействительность цепочки.
            if current_block.hash_block()!=self.hash(previous_block):
                return False

            # Check if the proof of work is valid
            if not self.valid_proof(previous_block.proof, current_block.proof):
                return False

        return True

# Основная цель PoW - найти такое число (proof), что хеш от комбинации предыдущего доказательства (last_proof) и нового доказательства
# (proof) содержит ведущие четыре нуля.
    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work algorithm:
        - Find a number p' such that hash(pp') contains leading 4 zeros, where p is the previous p'
        - p is the previous proof, and p' is the new proof
        """
        proof=0
        while self.valid_proof(last_proof, proof) is False:
            proof+=1
        return proof
    
    # Переменная proof инициализируется значением 0, и алгоритм начинает поиск с этой точки.
    # С помощью цикла while проверяется, выполняется ли условие self.valid_proof(last_proof, proof) is False.
    # Это условие означает, что алгоритм будет продолжать поиск, пока не найдется доказательство, удовлетворяющее заданному критерию хеша с четырьмя ведущими нулями.
    # Как только подходящее доказательство найдено, оно возвращается из функции.

    @staticmethod
    # Это статический метод, который проверяет, является ли данное доказательство (proof) действительным, с учетом предыдущего доказательства (last_proof).
    # Для этой проверки выполняется следующее:
    # здается строка guess, которая представляет собой конкатенацию предыдущего доказательства и нового доказательства, преобразованных в байты.
    # Затем создается хеш (guess_hash) этой строки с использованием алгоритма SHA-256.
    # звращается True, если хеш начинается с четырех ведущих нулей (количество нулей можно настраивать в зависимости от желаемой сложности Proof of Work). В противном случае возвращается False.
    def valid_proof(last_proof, proof):
        guess=f'{last_proof}{proof}'.encode()
        guess_hash=hashlib.sha256(guess).hexdigest()
        # Adjust the difficulty as needed
        return guess_hash[:4]=='0000'
