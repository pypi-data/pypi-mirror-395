from wicspy.web.seawater_radiation import get_seawater_radiation

def radiation():
    data = get_seawater_radiation()
    print(f"If artificial gamma radionuclides are detected: {data}")

if __name__ == "__main__":
    radiation()
