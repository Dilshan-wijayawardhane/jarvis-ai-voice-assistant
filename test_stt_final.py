import speech_recognition as sr
import time

print("=" * 60)
print("SPEECH RECOGNITION FINAL TEST")
print("=" * 60)

# Use the same settings as JARVIS
r = sr.Recognizer()
r.energy_threshold = 300
r.dynamic_energy_threshold = True
r.dynamic_energy_adjustment_damping = 0.15
r.dynamic_energy_ratio = 1.5
r.pause_threshold = 0.3
r.phrase_threshold = 0.2
r.non_speaking_duration = 0.3

print("\nMicrophone index 1 - Testing...")

try:
    with sr.Microphone(device_index=1) as source:
        print("\n📢 Adjusting for ambient noise... (2 seconds)")
        r.adjust_for_ambient_noise(source, duration=2)
        print(f"✅ Energy threshold set to: {r.energy_threshold}")
        
        print("\n🎤 Speak a clear phrase now (you have 5 seconds)...")
        print("🎤 LISTENING...")
        
        # Listen with longer timeout
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        
        print("🎤 Audio captured! Sending to Google...")
        
        # Try to recognize
        text = r.recognize_google(audio)
        print(f"\n✅ SUCCESS! You said: '{text}'")
        
except sr.WaitTimeoutError:
    print("\n❌ TIMEOUT: No speech detected in 5 seconds")
    print("   Try speaking louder or closer to the microphone")
except sr.UnknownValueError:
    print("\n❌ COULD NOT UNDERSTAND: Audio was captured but not recognized")
    print("   Try speaking more clearly")
except sr.RequestError as e:
    print(f"\n❌ GOOGLE API ERROR: {e}")
    print("   Check your internet connection")
except Exception as e:
    print(f"\n❌ ERROR: {e}")