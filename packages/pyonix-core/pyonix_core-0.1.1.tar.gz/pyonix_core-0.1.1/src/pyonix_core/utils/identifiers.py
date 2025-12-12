class ISBN:
    @staticmethod
    def clean(isbn: str) -> str:
        """Removes hyphens and spaces."""
        if not isbn:
            return ""
        return isbn.replace("-", "").replace(" ", "").upper()

    @staticmethod
    def validate(isbn: str) -> bool:
        """Checks length and checksum."""
        clean = ISBN.clean(isbn)
        if len(clean) == 13:
            return ISBN._check_13(clean)
        elif len(clean) == 10:
            return ISBN._check_10(clean)
        return False

    @staticmethod
    def to_13(isbn10: str) -> str:
        """Converts valid ISBN-10 to ISBN-13."""
        clean = ISBN.clean(isbn10)
        if len(clean) != 10: 
            raise ValueError("Invalid length for ISBN-10")
        
        # Validate ISBN-10 checksum first? 
        # The plan implies we just convert. But let's be safe.
        if not ISBN._check_10(clean):
             raise ValueError("Invalid ISBN-10 checksum")

        prefix = "978" + clean[:-1]
        check = ISBN._calculate_checksum_13(prefix)
        return prefix + str(check)

    @staticmethod
    def _check_10(isbn: str) -> bool:
        if len(isbn) != 10:
            return False
        try:
            total = 0
            for i in range(9):
                total += int(isbn[i]) * (10 - i)
            
            last = isbn[9]
            if last == 'X':
                total += 10
            else:
                total += int(last)
            
            return total % 11 == 0
        except ValueError:
            return False

    @staticmethod
    def _check_13(isbn: str) -> bool:
        if len(isbn) != 13:
            return False
        try:
            total = 0
            for i in range(12):
                digit = int(isbn[i])
                if i % 2 == 0:
                    total += digit
                else:
                    total += digit * 3
            
            check = (10 - (total % 10)) % 10
            return check == int(isbn[12])
        except ValueError:
            return False

    @staticmethod
    def _calculate_checksum_13(prefix: str) -> int:
        # prefix should be 12 digits
        total = 0
        for i in range(12):
            digit = int(prefix[i])
            if i % 2 == 0:
                total += digit
            else:
                total += digit * 3
        
        return (10 - (total % 10)) % 10
