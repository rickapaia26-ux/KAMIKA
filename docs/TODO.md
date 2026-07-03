# KAMIKA - Tarefas Pendentes

## ✅ Concluído
- [x] Menu principal (YouTube/Rastrear)
- [x] Seleção idioma (Português/Inglês)
- [x] Download música (MP3)
- [x] Download vídeo (1080p)
- [x] Cortar por tempo
- [x] Menu pós-download (Abrir pasta/Voltar/Sair)
- [x] Validação de input em todos os menus
- [x] Separação de pastas (KAMIKA/KAMIKA Downloads)
- [x] Limpeza automática da pasta LOADING
- [x] Sistema de fallback para formatos de vídeo ★ NOVO
- [x] Preferências guardadas durante a sessão ★ NOVO

## 🔧 Melhorias Possíveis
- [ ] Adicionar opção de qualidade no vídeo

## 🐛 Bugs Conhecidos
- Nenhum reportado

## 📝 Notas
- Formato de tempo: MM:SS
- O script usa yt-dlp para downloads
- Sistema de fallback tenta 3 formatos automaticamente
- Playlist detection: `is_playlist()` so usado no YouTube (menu_youtube + rastrear->yt)
  As outras plataformas (Spotify, SoundCloud, Bandcamp...) tem detecao propria
  em `menu_rastrear()` e `detect_input()`. EXCECAO a regra geral.
