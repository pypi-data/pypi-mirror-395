"""
Hong Kong Observatory Seawater Radiation Monitoring Data Module
"""

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    raise ImportError(
        "To use the web module, you need to install the wicspy[web] extra.\n"
    )


def get_seawater_radiation():
    """
    Get artificial gamma radionuclide values from HKO seawater radiation monitoring data
    
    Returns:
        bool: Whether artificial gamma radionuclides are detected
    
    Raises:
        requests.RequestException: When network request fails
        ValueError: When page structure is unexpected
    """
    url = "https://www.hko.gov.hk/tc/radiation/monitoring/seawater.html"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all rows in the table
        rows = soup.find('table').find_all('tr')[3:]  # Skip header
        
        is_detected = False
        
        for row in rows:
            cols = row.find_all('td')
            radiation = cols[2].text.strip()  # Artificial gamma radionuclide value
            if radiation != '沒有檢出':  # Not detected
                is_detected = True
                break
        
        return is_detected
        
    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to fetch data: {e}")
    except (AttributeError, IndexError) as e:
        raise ValueError(f"Failed to parse page structure: {e}")


if __name__ == "__main__":
    try:
        data = get_seawater_radiation()
        print(data)
    except Exception as e:
        print(f"Error: {e}") 