# KAMIKA v2.1

## Estrutura do Projeto

```
KAMIKA-PROJECT/
├── kamika.py          # Script principal
├── KAMIKA.bat         # Ficheiro de inicialização
├── LOADING/           # Downloads temporários (limpo automaticamente)
└── docs/              # Documentação
    └── README.md      # Este ficheiro
```

**KAMIKA/** (Desktop) - Downloads finais apenas

## Funcionalidades

### YouTube
- **Música** - Descarrega áudio em MP3
- **Vídeo** - Descarrega vídeo em MP4 (1080p)
- **Cortar** - Opção de cortar por tempo

### Rastrear
- Aceita links de qualquer plataforma
- YouTube → descarrega direto como música
- Spotify/SoundCloud/etc → procura no YouTube

## Comandos Úteis

```bash
# Executar o script
python kamika.py

# Ou clicar no KAMIKA.bat
```

## Notas

- Formato de tempo: MM:SS
- Qualidade vídeo: 1080p (melhor disponível)
- Qualidade música: MP3 (melhor disponível)
- A pasta LOADING é limpa automaticamente após cada download
