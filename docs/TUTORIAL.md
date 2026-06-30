# KAMIKA - Tutorial

## Como Usar

### 1. Iniciar o Programa
- Clique duplo em `KAMIKA.bat`
- Ou execute: `python kamika.py`

### 2. Escolher Idioma
- **[1] Português** - Menu em português
- **[2] English** - Menu em inglês
- **[0] Exit** - Sair do programa

### 3. Menu Principal
- **YouTube** - Descarregar de links do YouTube
- **Rastrear** - Procurar músicas em várias plataformas

---

## YouTube

### Opção 1: Música
1. Cole o link do YouTube
2. Escolha **[1] Música**
3. Escolha **[1] Completa** ou **[2] Cortar**
4. Se cortar, indique o tempo (MM:SS)
5. Confirme com **S**

### Opção 2: Vídeo
1. Cole o link do YouTube
2. Escolha **[2] Vídeo**
3. Escolha **[1] Completo** ou **[2] Cortar**
4. Se cortar, indique o tempo (MM:SS)
5. Confirme com **S**

---

## Rastrear

### Plataformas Suportadas
- YouTube
- Spotify (procura no YouTube)
- SoundCloud
- Bandcamp
- Audiomack
- Outros links diretos

### Como Usar
1. Cole o link ou escreva o nome da música
2. O programa deteta automaticamente a plataforma
3. Confirme o download

---

## Formato de Tempo

- **MM:SS** - Exemplo: `1:30` (1 minuto e 30 segundos)
- **H:MM:SS** - Exemplo: `1:30:00` (1 hora, 30 minutos)

---

## Menu Pós-Download

Após o download terminar:
- **[1] Abrir pasta** - Abre a pasta KAMIKA Downloads
- **[2] Voltar ao início** - Volta ao menu principal
- **[3] Sair** - Fecha o programa

---

## Estrutura de Pastas

```
KAMIKA Downloads\
├── (músicas em MP3)
└── (vídeos em MP4)

KAMIKA\
├── kamika.py
├── KAMIKA.bat
├── LOADING\ (temporário)
└── docs\
```

---

## Dicas

- Use **[0] Voltar** em qualquer menu para recuar
- O botão **N** no download cancela e volta ao menu anterior
- A pasta LOADING é limpa automaticamente
- Os downloads ficam em `KAMIKA Downloads` no Desktop
