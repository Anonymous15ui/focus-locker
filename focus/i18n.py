"""Everything the UI says, in every supported language.

To add a language: add it to LANGUAGES (and RTL if it reads right to left), then
copy the "en" block in STRINGS and translate it. Any key a language is missing
falls back to English, so a half-done translation still works.
"""
LANGUAGES = {
    "en": "English",
    "ar": "العربية",
    "fr": "Français",
    "es": "Español",
}
RTL = {"ar"}

STRINGS = {
    "en": {
        "title": "Focus Locker",
        "start": "Start focus",
        "break_now": "Break now",
        "stop": "Stop / unlock",
        "status_focus": "LOCKED - {n} task(s) left",
        "status_break": "BREAK - {m}:{s} left ({reason})",
        "status_idle": "Unlocked - not in a focus session",
        "ring_focus_sub": "done",
        "ring_break_sub": "break",
        "ring_idle_sub": "ready",
        "progress": "{done} of {total} done",
        "headline_focus": "Locked in",
        "headline_break": "Breathe",
        "headline_idle": "Ready when you are",
        "theme_dark": "Dark mode",
        "scheme": "Colour scheme",
        "theme_light": "Light mode",
        "reason_task": "task finished",
        "reason_list": "list finished",
        "reason_manual": "manual break",
        # to-do
        "tab_todo": "To-do",
        "task": "Task",
        "link_optional": "Link (optional)",
        "add": "Add",
        "link_hint": "A link can be a website, or a folder or file on this computer - "
                     "wherever the task actually gets done.",
        "mark_done": "Mark done (starts break)",
        "open_link": "Open link",
        "edit_link": "Edit link",
        "undo_done": "Undo done",
        "delete": "Delete",
        # lists
        "tab_blocked_apps": "Blocked apps",
        "hint_blocked_apps": "Process name as it appears in Task Manager, e.g. chrome.exe",
        "tab_blocked_sites": "Blocked sites",
        "hint_blocked_sites": "Domain only, e.g. youtube.com (www. is added for you)",
        "tab_allowed_sites": "Always allowed sites",
        "hint_allowed_sites": "Never blocked, e.g. your school portal: myschool.edu",
        "remove_selected": "Remove selected",
        # habits
        "tab_habits": "Habits",
        "habit": "Habit",
        "habit_toggle": "Done today / undo",
        "habit_hint": "Tick each habit off once a day. The dots are the last 7 days, "
                      "oldest first.",
        "habit_streak": "{n}-day streak",
        # settings
        "tab_settings": "Settings",
        "language": "Language",
        "set_each": "Take a break after each finished task",
        "set_each_min": "Break after each task (minutes)",
        "set_list_on": "Take a longer break when the whole list is finished",
        "set_list_min": "Break after whole list (minutes)",
        "set_mode": "How blocked apps are handled",
        "mode_suspend": "suspend",
        "mode_close": "close",
        "mode_hint": "suspend = freeze the app, nothing is lost (recommended)\n"
                     "close = terminate it, unsaved work may be lost",
        "set_sites": "Also block websites (needs the app run as administrator)",
        "set_close_browsers": "Close browsers when locking (otherwise an open "
                              "YouTube tab keeps playing for minutes)",
        "set_poll": "Check for blocked apps every (seconds)",
        "save_settings": "Save settings",
        "tab_activity": "Activity",
        # dialogs and log lines
        "no_link_title": "No link",
        "open_failed_title": "Could not open",
        "link_title": "Link",
        "link_prompt": "Where does this task get done?\n"
                       "A website, or a folder or file on this computer:",
        "nothing_title": "Nothing to do",
        "nothing_body": "Add at least one task first.",
        "sites_warn_title": "Websites will not be blocked",
        "sites_warn_body": "Editing the hosts file needs administrator rights.\n"
                           "Apps will still be locked. Restart the app as administrator "
                           "(run_as_admin.bat) to block websites too.",
        "bad_value_title": "Bad value",
        "bad_value_body": "Break lengths and interval must be numbers.",
        "still_locked_title": "Still locked",
        "still_locked_body": "Quitting will unlock everything. Quit anyway?",
        "not_admin": "Not running as administrator - website blocking will be skipped.",
        "settings_saved": "settings saved",
    },
    "ar": {
        "title": "قفل التركيز",
        "start": "ابدأ التركيز",
        "break_now": "استراحة الآن",
        "stop": "إيقاف / فتح القفل",
        "status_focus": "مقفل - المهام المتبقية: {n}",
        "status_break": "استراحة - متبقٍّ {m}:{s} ({reason})",
        "status_idle": "غير مقفل - لا توجد جلسة تركيز",
        "ring_focus_sub": "منجز",
        "ring_break_sub": "استراحة",
        "ring_idle_sub": "جاهز",
        "progress": "{done} من {total} منجزة",
        "headline_focus": "في تركيز",
        "headline_break": "خذ نفسًا",
        "headline_idle": "جاهز متى شئت",
        "theme_dark": "الوضع الداكن",
        "scheme": "نظام الألوان",
        "theme_light": "الوضع الفاتح",
        "reason_task": "انتهت مهمة",
        "reason_list": "انتهت القائمة",
        "reason_manual": "استراحة يدوية",
        "tab_todo": "المهام",
        "task": "المهمة",
        "link_optional": "الرابط (اختياري)",
        "add": "إضافة",
        "link_hint": "يمكن أن يكون الرابط موقعًا إلكترونيًا، أو مجلدًا أو ملفًا على هذا "
                     "الكمبيوتر - أينما تُنجَز المهمة فعلًا.",
        "mark_done": "تمّت (تبدأ الاستراحة)",
        "open_link": "فتح الرابط",
        "edit_link": "تعديل الرابط",
        "undo_done": "تراجع عن الإنجاز",
        "delete": "حذف",
        "tab_blocked_apps": "التطبيقات المحظورة",
        "hint_blocked_apps": "اسم العملية كما يظهر في مدير المهام، مثل chrome.exe",
        "tab_blocked_sites": "المواقع المحظورة",
        "hint_blocked_sites": "اسم النطاق فقط، مثل youtube.com (تُضاف www. تلقائيًا)",
        "tab_allowed_sites": "مواقع مسموحة دائمًا",
        "hint_allowed_sites": "لا تُحظر أبدًا، مثل بوابة مدرستك: myschool.edu",
        "remove_selected": "إزالة المحدد",
        "tab_habits": "العادات",
        "habit": "العادة",
        "habit_toggle": "أنجزتها اليوم / تراجع",
        "habit_hint": "علّم على كل عادة مرة واحدة في اليوم. النقاط هي آخر 7 أيام، "
                      "من الأقدم إلى الأحدث.",
        "habit_streak": "أيام متتالية: {n}",
        "tab_settings": "الإعدادات",
        "language": "اللغة",
        "set_each": "خذ استراحة بعد كل مهمة منجزة",
        "set_each_min": "مدة الاستراحة بعد كل مهمة (بالدقائق)",
        "set_list_on": "خذ استراحة أطول عند إنهاء القائمة كلها",
        "set_list_min": "مدة الاستراحة بعد القائمة كلها (بالدقائق)",
        "set_mode": "طريقة التعامل مع التطبيقات المحظورة",
        "mode_suspend": "تجميد",
        "mode_close": "إغلاق",
        "mode_hint": "تجميد = إيقاف التطبيق مؤقتًا دون فقدان أي شيء (مُستحسن)\n"
                     "إغلاق = إنهاء التطبيق، وقد يضيع العمل غير المحفوظ",
        "set_sites": "حظر المواقع أيضًا (يتطلب تشغيل التطبيق كمسؤول)",
        "set_close_browsers": "إغلاق المتصفحات عند القفل (وإلا يستمر تبويب يوتيوب "
                              "المفتوح في التشغيل لدقائق)",
        "set_poll": "التحقق من التطبيقات المحظورة كل (ثانية)",
        "save_settings": "حفظ الإعدادات",
        "tab_activity": "النشاط",
        "no_link_title": "لا يوجد رابط",
        "open_failed_title": "تعذّر الفتح",
        "link_title": "الرابط",
        "link_prompt": "أين تُنجَز هذه المهمة؟\n"
                       "موقع إلكتروني، أو مجلد أو ملف على هذا الكمبيوتر:",
        "nothing_title": "لا شيء للقيام به",
        "nothing_body": "أضف مهمة واحدة على الأقل أولًا.",
        "sites_warn_title": "لن يتم حظر المواقع",
        "sites_warn_body": "تعديل ملف hosts يحتاج إلى صلاحيات المسؤول.\n"
                           "ستبقى التطبيقات مقفلة. أعد تشغيل التطبيق كمسؤول "
                           "(run_as_admin.bat) لحظر المواقع أيضًا.",
        "bad_value_title": "قيمة غير صالحة",
        "bad_value_body": "يجب أن تكون مدد الاستراحة وفترة التحقق أرقامًا.",
        "still_locked_title": "ما زال مقفلًا",
        "still_locked_body": "الخروج سيفتح القفل عن كل شيء. هل تريد الخروج على أي حال؟",
        "not_admin": "التطبيق لا يعمل كمسؤول - سيتم تخطي حظر المواقع.",
        "settings_saved": "تم حفظ الإعدادات",
    },
    "fr": {
        "title": "Focus Locker",
        "start": "Démarrer le focus",
        "break_now": "Pause maintenant",
        "stop": "Arrêter / déverrouiller",
        "status_focus": "VERROUILLÉ - {n} tâche(s) restante(s)",
        "status_break": "PAUSE - encore {m}:{s} ({reason})",
        "status_idle": "Déverrouillé - aucune session de focus",
        "ring_focus_sub": "faites",
        "ring_break_sub": "pause",
        "ring_idle_sub": "prêt",
        "progress": "{done} sur {total} faites",
        "headline_focus": "Concentré",
        "headline_break": "Respire",
        "headline_idle": "Prêt quand tu veux",
        "theme_dark": "Mode sombre",
        "scheme": "Thème de couleurs",
        "theme_light": "Mode clair",
        "reason_task": "tâche terminée",
        "reason_list": "liste terminée",
        "reason_manual": "pause manuelle",
        "tab_todo": "À faire",
        "task": "Tâche",
        "link_optional": "Lien (facultatif)",
        "add": "Ajouter",
        "link_hint": "Un lien peut être un site web, ou un dossier ou fichier sur cet "
                     "ordinateur - là où la tâche se fait vraiment.",
        "mark_done": "Terminée (lance la pause)",
        "open_link": "Ouvrir le lien",
        "edit_link": "Modifier le lien",
        "undo_done": "Annuler terminée",
        "delete": "Supprimer",
        "tab_blocked_apps": "Applis bloquées",
        "hint_blocked_apps": "Nom du processus tel qu'affiché dans le Gestionnaire des "
                             "tâches, ex. chrome.exe",
        "tab_blocked_sites": "Sites bloqués",
        "hint_blocked_sites": "Domaine seulement, ex. youtube.com (www. est ajouté pour vous)",
        "tab_allowed_sites": "Sites toujours autorisés",
        "hint_allowed_sites": "Jamais bloqués, ex. le portail de votre école : myschool.edu",
        "remove_selected": "Retirer la sélection",
        "tab_habits": "Habitudes",
        "habit": "Habitude",
        "habit_toggle": "Fait aujourd'hui / annuler",
        "habit_hint": "Cochez chaque habitude une fois par jour. Les points sont les "
                      "7 derniers jours, du plus ancien au plus récent.",
        "habit_streak": "série de {n} jour(s)",
        "tab_settings": "Paramètres",
        "language": "Langue",
        "set_each": "Faire une pause après chaque tâche terminée",
        "set_each_min": "Pause après chaque tâche (minutes)",
        "set_list_on": "Faire une pause plus longue quand toute la liste est terminée",
        "set_list_min": "Pause après la liste entière (minutes)",
        "set_mode": "Traitement des applis bloquées",
        "mode_suspend": "suspendre",
        "mode_close": "fermer",
        "mode_hint": "suspendre = geler l'appli, rien n'est perdu (recommandé)\n"
                     "fermer = la terminer, le travail non enregistré peut être perdu",
        "set_sites": "Bloquer aussi les sites web (l'appli doit tourner en administrateur)",
        "set_close_browsers": "Fermer les navigateurs au verrouillage (sinon un onglet "
                              "YouTube ouvert continue de jouer pendant des minutes)",
        "set_poll": "Vérifier les applis bloquées toutes les (secondes)",
        "save_settings": "Enregistrer",
        "tab_activity": "Activité",
        "no_link_title": "Pas de lien",
        "open_failed_title": "Impossible d'ouvrir",
        "link_title": "Lien",
        "link_prompt": "Où cette tâche se fait-elle ?\n"
                       "Un site web, ou un dossier ou fichier sur cet ordinateur :",
        "nothing_title": "Rien à faire",
        "nothing_body": "Ajoutez d'abord au moins une tâche.",
        "sites_warn_title": "Les sites ne seront pas bloqués",
        "sites_warn_body": "Modifier le fichier hosts demande les droits administrateur.\n"
                           "Les applis seront quand même verrouillées. Relancez l'appli en "
                           "administrateur (run_as_admin.bat) pour bloquer aussi les sites.",
        "bad_value_title": "Valeur invalide",
        "bad_value_body": "Les durées de pause et l'intervalle doivent être des nombres.",
        "still_locked_title": "Toujours verrouillé",
        "still_locked_body": "Quitter va tout déverrouiller. Quitter quand même ?",
        "not_admin": "Pas lancé en administrateur - le blocage des sites sera ignoré.",
        "settings_saved": "paramètres enregistrés",
    },
    "es": {
        "title": "Focus Locker",
        "start": "Iniciar enfoque",
        "break_now": "Descanso ahora",
        "stop": "Detener / desbloquear",
        "status_focus": "BLOQUEADO - quedan {n} tarea(s)",
        "status_break": "DESCANSO - quedan {m}:{s} ({reason})",
        "status_idle": "Desbloqueado - sin sesión de enfoque",
        "ring_focus_sub": "hechas",
        "ring_break_sub": "descanso",
        "ring_idle_sub": "listo",
        "progress": "{done} de {total} hechas",
        "headline_focus": "Concentrado",
        "headline_break": "Respira",
        "headline_idle": "Listo cuando quieras",
        "theme_dark": "Modo oscuro",
        "scheme": "Esquema de color",
        "theme_light": "Modo claro",
        "reason_task": "tarea terminada",
        "reason_list": "lista terminada",
        "reason_manual": "descanso manual",
        "tab_todo": "Pendientes",
        "task": "Tarea",
        "link_optional": "Enlace (opcional)",
        "add": "Añadir",
        "link_hint": "Un enlace puede ser un sitio web, o una carpeta o archivo en este "
                     "equipo - donde realmente se hace la tarea.",
        "mark_done": "Hecha (inicia descanso)",
        "open_link": "Abrir enlace",
        "edit_link": "Editar enlace",
        "undo_done": "Deshacer hecha",
        "delete": "Eliminar",
        "tab_blocked_apps": "Apps bloqueadas",
        "hint_blocked_apps": "Nombre del proceso como aparece en el Administrador de "
                             "tareas, p. ej. chrome.exe",
        "tab_blocked_sites": "Sitios bloqueados",
        "hint_blocked_sites": "Solo el dominio, p. ej. youtube.com (www. se añade solo)",
        "tab_allowed_sites": "Sitios siempre permitidos",
        "hint_allowed_sites": "Nunca se bloquean, p. ej. el portal de tu escuela: "
                              "myschool.edu",
        "remove_selected": "Quitar selección",
        "tab_habits": "Hábitos",
        "habit": "Hábito",
        "habit_toggle": "Hecho hoy / deshacer",
        "habit_hint": "Marca cada hábito una vez al día. Los puntos son los últimos "
                      "7 días, del más antiguo al más reciente.",
        "habit_streak": "racha de {n} día(s)",
        "tab_settings": "Ajustes",
        "language": "Idioma",
        "set_each": "Descansar después de cada tarea terminada",
        "set_each_min": "Descanso tras cada tarea (minutos)",
        "set_list_on": "Descanso más largo al terminar toda la lista",
        "set_list_min": "Descanso tras toda la lista (minutos)",
        "set_mode": "Qué hacer con las apps bloqueadas",
        "mode_suspend": "suspender",
        "mode_close": "cerrar",
        "mode_hint": "suspender = congelar la app, no se pierde nada (recomendado)\n"
                     "cerrar = terminarla, el trabajo sin guardar puede perderse",
        "set_sites": "Bloquear también sitios web (la app debe ejecutarse como administrador)",
        "set_close_browsers": "Cerrar navegadores al bloquear (si no, una pestaña de "
                              "YouTube abierta sigue reproduciéndose varios minutos)",
        "set_poll": "Buscar apps bloqueadas cada (segundos)",
        "save_settings": "Guardar ajustes",
        "tab_activity": "Actividad",
        "no_link_title": "Sin enlace",
        "open_failed_title": "No se pudo abrir",
        "link_title": "Enlace",
        "link_prompt": "¿Dónde se hace esta tarea?\n"
                       "Un sitio web, o una carpeta o archivo en este equipo:",
        "nothing_title": "Nada que hacer",
        "nothing_body": "Añade al menos una tarea primero.",
        "sites_warn_title": "Los sitios web no se bloquearán",
        "sites_warn_body": "Editar el archivo hosts requiere permisos de administrador.\n"
                           "Las apps se bloquearán igualmente. Reinicia la app como "
                           "administrador (run_as_admin.bat) para bloquear también los sitios.",
        "bad_value_title": "Valor no válido",
        "bad_value_body": "Las duraciones de descanso y el intervalo deben ser números.",
        "still_locked_title": "Sigue bloqueado",
        "still_locked_body": "Salir desbloqueará todo. ¿Salir de todos modos?",
        "not_admin": "No se ejecuta como administrador - se omitirá el bloqueo de sitios.",
        "settings_saved": "ajustes guardados",
    },
}

_current = "en"


def set_language(code):
    global _current
    _current = code if code in LANGUAGES else "en"


def current():
    return _current


def is_rtl():
    return _current in RTL


def t(key, **values):
    """The text for `key` in the current language, falling back to English."""
    text = STRINGS.get(_current, {}).get(key) or STRINGS["en"][key]
    return text.format(**values) if values else text
