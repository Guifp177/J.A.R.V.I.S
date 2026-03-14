import json
import queue
from pathlib import Path

import numpy as np
import sounddevice as sd
import torch
from faster_whisper import WhisperModel
from vosk import KaldiRecognizer, Model


class MicInput:
    def __init__(self):
        print("\n" + "=" * 40)
        print("[JARVIS - SYSTEM] Inicializando Módulos de Áudio...")

        self.sample_rate = 16000

        try:
            print("[DEBUG] Carregando Silero VAD (IA de detecção de voz)...")
            self.vad_model, utils = torch.hub.load(
                repo_or_dir="snakers4/silero-vad",
                model="silero_vad",
                force_reload=False,
            )
            self.has_vad = True
            print("[SUCCESS] VAD carregado com sucesso.")
        except Exception as e:
            print(f"[ERROR] Falha ao carregar VAD: {e}")
            self.has_vad = False

        try:
            print("[DEBUG] Inicializando Faster-Whisper (Modelo Tiny)...")
            # Para usar GPU NVIDIA: device="cuda", compute_type="float16"
            self.whisper_model = WhisperModel("tiny", device="cpu", compute_type="int8")
            self.has_whisper = True
            print("[SUCCESS] Faster-Whisper pronto.")
        except Exception as e:
            print(f"[WARNING] Whisper falhou: {e}")
            self.has_whisper = False

        model_path = Path("voice/models/vosk-pt")
        if model_path.exists():
            print(f"[DEBUG] Carregando modelo Vosk de: {model_path}")
            self.vosk_model = Model(str(model_path))
            self.has_vosk = True
            print("[SUCCESS] Vosk carregado como reserva.")
        else:
            self.has_vosk = False
            print("[WARNING] Vosk não encontrado. Sem modo reserva.")

        print("=" * 40 + "\n")

    def listen(self, max_seconds=30):
        """
        Escuta inteligente:
        - Desiste em 5s se ninguém falar nada.
        - Se falar, grava até terminar a frase ou bater o limite (30s).
        """
        print(f"[MIC] Ouvido aberto... (Max: {max_seconds}s)")
        audio_buffer = []
        is_speaking = False
        silent_chunks = 0
        chunks_processed = 0

        chunk_size = 512  # Recomendado para o Silero VAD
        # ~31 chunks por segundo. 155 chunks = 5 segundos.
        initial_timeout_limit = 155
        max_chunks = int((self.sample_rate * max_seconds) / chunk_size)

        try:
            with sd.InputStream(
                samplerate=self.sample_rate, channels=1, dtype="float32"
            ) as stream:
                while chunks_processed < max_chunks:
                    chunk, _ = stream.read(chunk_size)
                    chunks_processed += 1
                    chunk_flat = chunk.flatten()

                    if self.has_vad:
                        input_tensor = torch.from_numpy(chunk_flat)
                        speech_prob = self.vad_model(
                            input_tensor, self.sample_rate
                        ).item()

                        if speech_prob > 0.6:  # Limiar de sensibilidade
                            if not is_speaking:
                                print(
                                    f"[DEBUG] Voz detectada após {chunks_processed / 31:.1f}s!"
                                )
                                is_speaking = True
                            audio_buffer.append(chunk_flat)
                            silent_chunks = 0

                        elif is_speaking:
                            audio_buffer.append(chunk_flat)
                            silent_chunks += 1

                            # Se o silêncio durar ~0.6s (18 chunks), assume que terminou a frase
                            if silent_chunks > 18:
                                print("[DEBUG] Fim de frase detectado pelo silêncio.")
                                break

                        else:
                            # Caso ainda não tenha falado nada: verifica timeout de 5 segundos
                            if chunks_processed > initial_timeout_limit:
                                print(
                                    "[DEBUG] Ninguém falou nada por 5s. Encerrando..."
                                )
                                return ""
                    else:
                        # Fallback se o VAD falhar: grava direto
                        audio_buffer.append(chunk_flat)

            if not audio_buffer:
                return ""

            print(
                f"[DEBUG] Processando {len(audio_buffer) * chunk_size / self.sample_rate:.1f}s de áudio..."
            )
            full_audio = np.concatenate(audio_buffer)

            # --- TENTATIVA 1: WHISPER ---
            if self.has_whisper:
                print("[DEBUG] Transcrevendo com Faster-Whisper...")
                segments, _ = self.whisper_model.transcribe(
                    full_audio, language="pt", beam_size=5
                )
                text = " ".join([seg.text for seg in segments]).strip()
                if text:
                    print(f"[RESULTADO WHISPER] -> {text}")
                    return text

            # --- TENTATIVA 2: VOSK (meio ruim mas quebra galho) ---
            if self.has_vosk:
                print("[DEBUG] Whisper vazio. Usando Vosk...")
                int_audio = (full_audio * 32767).astype(np.int16)
                rec = KaldiRecognizer(self.vosk_model, self.sample_rate)
                rec.AcceptWaveform(int_audio.tobytes())
                text_vosk = json.loads(rec.FinalResult()).get("text", "").strip()
                print(f"[RESULTADO VOSK] -> {text_vosk}")
                return text_vosk

            return ""

        except Exception as e:
            print(f"[CRITICAL ERROR] Falha no sistema de microfone: {e}")
            return ""
