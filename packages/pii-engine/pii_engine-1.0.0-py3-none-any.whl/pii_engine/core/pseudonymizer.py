"""
Pseudonymization module for PII data.

Provides deterministic fake data generation for different PII types.
"""

import hashlib
from typing import Optional


class Pseudonymizer:
    """Handles pseudonymization of PII data for display purposes."""
    
    def __init__(self):
        """Initialize pseudonymizer with fake data pools."""
        self.fake_first_names = [
            "Alex", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Avery", "Quinn",
            "Blake", "Cameron", "Drew", "Emery", "Finley", "Harper", "Hayden", "Jamie"
        ]
        
        self.fake_last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas"
        ]
        
        self.fake_domains = [
            "example.com", "test.org", "demo.net", "sample.co", "mock.io", 
            "fake.edu", "pseudo.gov", "anon.biz"
        ]
        
        self.fake_companies = [
            "TechCorp", "DataSystems", "InfoSolutions", "GlobalTech", "MetaCorp",
            "CyberInc", "DigitalWorks", "CloudSoft", "NetDynamics", "SystemsPlus"
        ]
        
        self.fake_streets = [
            "Main St", "Oak Ave", "Pine Rd", "Elm Dr", "Cedar Ln", "Maple Way",
            "First St", "Second Ave", "Park Blvd", "Hill Rd", "Lake Dr", "River St"
        ]
        
        self.fake_cities = [
            "Springfield", "Franklin", "Georgetown", "Madison", "Riverside", "Fairview",
            "Midtown", "Oakville", "Hillside", "Lakewood", "Greenfield", "Westfield"
        ]
        
        self.fake_states = ["CA", "NY", "TX", "FL", "IL", "PA", "OH", "GA", "NC", "MI"]
    
    def _deterministic_choice(self, seed: str, choices: list) -> str:
        """Select from list using deterministic hash-based seed."""
        hash_val = int(hashlib.md5(seed.encode()).hexdigest()[:8], 16)
        return choices[hash_val % len(choices)]
    
    def _deterministic_number(self, seed: str, min_val: int, max_val: int) -> int:
        """Generate deterministic number in range using hash-based seed."""
        hash_val = int(hashlib.md5(seed.encode()).hexdigest()[:8], 16)
        return min_val + (hash_val % (max_val - min_val + 1))
    
    def pseudonymize(self, value: Optional[str], pii_type: str) -> Optional[str]:
        """
        Return a pseudonymized version based on PII data type.
        
        Args:
            value: The plaintext value to pseudonymize
            pii_type: Type of PII (email, phone, etc.)
            
        Returns:
            Pseudonymized version of the value
        """
        if value is None:
            return None
        
        pii_type = pii_type.lower()
        
        # Map data types to pseudonymization functions
        pseudonym_map = {
            "email": self._pseudonymize_email,
            "phone": self._pseudonymize_phone,
            "person_name": self._pseudonymize_person_name,
            "company_name": self._pseudonymize_company_name,
            "address": self._pseudonymize_address,
            "ssn": self._pseudonymize_ssn,
            "credit_card": self._pseudonymize_credit_card,
            "ip_address": self._pseudonymize_ip_address,
            "date_of_birth": lambda x: "1990-01-01",  # Generic fake date
            "generic_text": lambda x: "Anonymous Data",
        }
        
        pseudonym_func = pseudonym_map.get(pii_type, lambda x: "***")
        return pseudonym_func(value)
    
    def _pseudonymize_email(self, email: str) -> str:
        """Generate consistent fake email."""
        if not email or "@" not in email:
            return "user@example.com"
        
        # Use original email as seed for consistency
        seed = f"email_{email}"
        fake_user = self._deterministic_choice(seed + "_user", 
                                            [f"user{i:03d}" for i in range(100, 1000)])
        fake_domain = self._deterministic_choice(seed + "_domain", self.fake_domains)
        
        return f"{fake_user}@{fake_domain}"
    
    def _pseudonymize_phone(self, phone: str) -> str:
        """Generate consistent fake phone number."""
        if not phone:
            return "555-0100"
        
        seed = f"phone_{phone}"
        area_code = self._deterministic_number(seed + "_area", 200, 999)
        exchange = self._deterministic_number(seed + "_exchange", 200, 999)
        number = self._deterministic_number(seed + "_number", 1000, 9999)
        
        return f"{area_code}-{exchange}-{number}"
    
    def _pseudonymize_person_name(self, name: str) -> str:
        """Generate consistent fake person name."""
        if not name:
            return "John Doe"
        
        seed = f"name_{name}"
        fake_first = self._deterministic_choice(seed + "_first", self.fake_first_names)
        fake_last = self._deterministic_choice(seed + "_last", self.fake_last_names)
        
        return f"{fake_first} {fake_last}"
    
    def _pseudonymize_company_name(self, company: str) -> str:
        """Generate consistent fake company name."""
        if not company:
            return "TechCorp Inc"
        
        seed = f"company_{company}"
        fake_company = self._deterministic_choice(seed, self.fake_companies)
        suffix = self._deterministic_choice(seed + "_suffix", ["Inc", "LLC", "Corp", "Ltd"])
        
        return f"{fake_company} {suffix}"
    
    def _pseudonymize_address(self, address: str) -> str:
        """Generate consistent fake address."""
        if not address:
            return "123 Main St, Springfield, CA 90210"
        
        seed = f"address_{address}"
        number = self._deterministic_number(seed + "_number", 100, 9999)
        street = self._deterministic_choice(seed + "_street", self.fake_streets)
        city = self._deterministic_choice(seed + "_city", self.fake_cities)
        state = self._deterministic_choice(seed + "_state", self.fake_states)
        zip_code = self._deterministic_number(seed + "_zip", 10000, 99999)
        
        return f"{number} {street}, {city}, {state} {zip_code}"
    
    def _pseudonymize_ssn(self, ssn: str) -> str:
        """Generate consistent fake SSN."""
        if not ssn:
            return "123-45-6789"
        
        seed = f"ssn_{ssn}"
        area = self._deterministic_number(seed + "_area", 100, 999)
        group = self._deterministic_number(seed + "_group", 10, 99)
        serial = self._deterministic_number(seed + "_serial", 1000, 9999)
        
        return f"{area:03d}-{group:02d}-{serial:04d}"
    
    def _pseudonymize_credit_card(self, cc: str) -> str:
        """Generate consistent fake credit card."""
        if not cc:
            return "4532-1234-5678-9012"
        
        seed = f"cc_{cc}"
        # Generate fake 16-digit number starting with 4 (Visa-like)
        digits = "4" + "".join([str(self._deterministic_number(seed + f"_{i}", 0, 9)) for i in range(15)])
        
        return f"{digits[:4]}-{digits[4:8]}-{digits[8:12]}-{digits[12:16]}"
    
    def _pseudonymize_ip_address(self, ip: str) -> str:
        """Generate consistent fake IP address."""
        if not ip:
            return "192.168.1.100"
        
        seed = f"ip_{ip}"
        octets = [self._deterministic_number(seed + f"_{i}", 1, 254) for i in range(4)]
        
        return ".".join(map(str, octets))