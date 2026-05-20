import os
import urllib.request

def setup_images():
    os.makedirs("images", exist_ok=True)
    
    images_to_download = {
        "images/samsung.jpg": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?auto=format&fit=crop&w=500&q=80",
        "images/apple.jpg": "https://images.unsplash.com/photo-1695048064973-10023a8edccf?auto=format&fit=crop&w=500&q=80",
        "images/tarte.jpg": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?auto=format&fit=crop&w=500&q=80",
        "images/oysho.jpg": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?auto=format&fit=crop&w=500&q=80",
        "images/adidas.jpg": "https://images.unsplash.com/photo-1518002171953-a080ee817801?auto=format&fit=crop&w=500&q=80",
        "images/newbalance.jpg": "https://images.unsplash.com/photo-1539185441755-769473a23570?auto=format&fit=crop&w=500&q=80"
    }
    
    print("Resimler yerel 'images' klasorunuze yerlestiriliyor...\n")
    for filepath, url in images_to_download.items():
        print(f"Indiriliyor: {filepath}...")
        try:
            urllib.request.urlretrieve(url, filepath)
        except Exception as e:
            print(f"Hata: {e}")
            
if __name__ == "__main__":
    setup_images()
    print("\nIslem tamam! Tum resimler klasore eklendi. Tarayicida sayfayi yenileyebilirsiniz. 🎉")