import os
import re
import httpx
import asyncio
from bs4 import BeautifulSoup
from rich.console import Console
from playwright.async_api import async_playwright

console = Console()

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def extract_chapter_number(title):
    match = re.search(r'chap(?:ter)?\s*(\d+)', title, re.IGNORECASE)
    return f"Chapter {match.group(1).zfill(2)}" if match else "Chapter Unknown"

async def download_manga(url):
    try:
        async with async_playwright() as p:
            # Jalankan browser agar bisa render penuh (non-headless untuk debugging)
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto(url, wait_until='domcontentloaded')

            console.print("[cyan]📜 Halaman dibuka, memuat gambar...[/cyan]")

            # Scroll bertahap agar semua gambar lazyload muncul
            for y in range(0, 8000, 500):
                await page.evaluate(f"window.scrollTo(0, {y})")
                await asyncio.sleep(1.5)

            await asyncio.sleep(3)
            html = await page.content()
            await browser.close()

        # Simpan hasil HTML untuk debugging
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(html)
        console.print("[yellow]HTML hasil render disimpan ke debug.html[/yellow]")

        # Parsing HTML
        soup = BeautifulSoup(html, 'html.parser')
        title_tag = soup.find('title')
        full_title = title_tag.text.strip() if title_tag else "Untitled Manga"

        manga_name = re.sub(r'\s*chap(?:ter)?\s*\d+.*', '', full_title, flags=re.IGNORECASE).strip()
        chapter_name = extract_chapter_number(full_title)

        folder_name = sanitize_filename(f"{manga_name} ({chapter_name})")
        os.makedirs(folder_name, exist_ok=True)

        # Ambil gambar dari atribut data-srcset, srcset, atau data-src
        images = soup.find_all('img', class_=lambda c: c and 'chapter-img' in c)
        img_urls = []

        for img in images:
            for attr in ['data-srcset', 'srcset', 'data-src']:
                url = img.get(attr)
                if url and 'loading.gif' not in url:
                    img_urls.append(url)
                    break

        if not img_urls:
            console.print("[red]❌ Tidak ada gambar ditemukan meski sudah dirender dan discroll![/red]")
            return

        console.print(f"[cyan]Manga:[/cyan] {manga_name}")
        console.print(f"[cyan]Chapter:[/cyan] {chapter_name}")
        console.print(f"[cyan]Total gambar ditemukan:[/cyan] {len(img_urls)}")

        # Unduh gambar secara async
        async with httpx.AsyncClient() as client:
            for i, img_url in enumerate(img_urls, 1):
                try:
                    response = await client.get(img_url)
                    response.raise_for_status()
                    filename = os.path.join(folder_name, f"{chapter_name} - {str(i).zfill(3)}.jpg")
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    console.print(f"[green]✅ {chapter_name} - {str(i).zfill(3)} : Sukses[/green]")
                except Exception as e:
                    console.print(f"[red]❌ {chapter_name} - {str(i).zfill(3)} : Gagal - {e}[/red]")

        console.print(f"[bold green]🎉 Selesai! Semua gambar disimpan di folder: {folder_name}[/bold green]")

    except Exception as e:
        console.print(f"[bold red]Terjadi kesalahan: {e}[/bold red]")

def main():
    while True:
        url = input("Masukan URL chapter: ").strip()
        asyncio.run(download_manga(url))
        lanjut = input("Ingin melanjutkan? (Ya/Tidak): ").lower()
        if lanjut != 'ya':
            print("Terima kasih. Selamat tinggal!")
            break

if __name__ == "__main__":
    main()
