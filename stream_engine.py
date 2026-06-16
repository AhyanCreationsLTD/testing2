import os
import subprocess

# গিটহাব ওয়ার্কফ্লো থেকে ডাইনামিক ইনপুট রিসিভ করা
VIDEO_URL = os.getenv("VIDEO_URL")
RTMP_TARGET = os.getenv("RTMP_TARGET")

# 🔗 আপনার কাস্টম অ্যাড এবং ঘড়ির ফাইলের ডিরেক্ট ইউআরএল (প্রয়োজন হলে এখান থেকে চেঞ্জ করতে পারবেন)
ADS_URL = "https://stream.ahyancreations.top/ads.mp4"    
WATCH_URL = "https://stream.ahyancreations.top/watch.gif" 

# ⏱️ গ্লোবাল কনফিগারেশন 
AD_DURATION = 5      # অ্যাডটি ঠিক কত সেকেন্ড স্ক্রিনে ভেসে থাকবে (৫ সেকেন্ড)
AD_INTERVAL = 1800   # প্রতি কত সেকেন্ড পর পর অ্যাড শো করবে (১৮০০ সেকেন্ড = ৩০ মিনিট)

print("📥 ক্লাউড থেকে প্রয়োজনীয় মিডিয়া ফাইল ডাউনলোড করা হচ্ছে...")
subprocess.run(f"curl -L -o main_video.mp4 '{VIDEO_URL}'", shell=True)
subprocess.run(f"curl -L -o ads.mp4 '{ADS_URL}'", shell=True)
subprocess.run(f"curl -L -o watch.gif '{WATCH_URL}'", shell=True)

print("🚀 ২৪/৭ নন-স্টপ লাইভ স্ট্রিমিং ও বট-বাইপাস ইঞ্জিন চালু হচ্ছে...")

# এফএফএমপেক মিক্সিং ও ওভারলে পাইপলাইন কমান্ড
cmd = (
    f"ffmpeg -re -stream_loop -1 -i main_video.mp4 "
    f"-ignore_loop 0 -i watch.gif "
    f"-stream_loop -1 -i ads.mp4 "
    f"-filter_complex \""
    f"[0:v][1:v]overlay=W-w-30:30[v_with_watch]; "
    f"[2:v]scale=400:-1[scaled_ads]; "
    f"[v_with_watch][scaled_ads]overlay=30:H-h-30:enable='between(mod(t,{AD_INTERVAL}),0,{AD_DURATION})'[outv]\" "
    f"-map \"[outv]\" -map \"0:a\" "
    f"-c:v libx264 -preset veryfast -b:v 3000k -maxrate 3000k -bufsize 6000k "
    f"-pix_fmt yuv420p -g 60 -c:a aac -b:a 128k -ar 44100 -f flv '{RTMP_TARGET}'"
)

# লাইভ রান প্রসেস ট্রিগার
subprocess.run(cmd, shell=True)