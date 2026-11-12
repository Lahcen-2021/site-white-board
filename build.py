#!/usr/bin/env python3
"""Builds the SiteWhiteboard static site into ./dist

  python3 build.py --domain https://your-domain.com --adsense ca-pub-1234567890123456 \
      --email contact@your-domain.com --checkout https://... --validate https://... --price "$4 / month"

Only --domain is needed for a first build. Everything else can be added later and rebuilt.
"""
import argparse, datetime, html, json, re, shutil
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
SRC, DIST = ROOT / "src", ROOT / "dist"
LANGS = ["en", "fr", "ar"]
UPDATED = {"en": "11 November 2026", "fr": "11 novembre 2026", "ar": "11 نوفمبر 2026"}

L = {
"en": dict(
  name="English", title="SiteWhiteboard – free online whiteboard, no sign-up",
  desc="A free online whiteboard with markers, sticky notes, shapes and arrows. No account, nothing to install. Your boards stay in your browser.",
  nav_feat="Features", nav_price="Pricing", nav_faq="Questions", open="Open a board",
  h1a="Open a whiteboard and ", h1b="start drawing", h1c=".",
  lead="SiteWhiteboard is a free online whiteboard with markers, sticky notes, shapes and arrows. No account, nothing to install. Your boards stay in your browser.",
  small="Free. Works on phone, tablet and computer.", hint="Try it here. Draw in this box.", clear="Clear", ad="Advertisement",
  feat_h="Everything a whiteboard needs",
  feats=[("Markers and eraser", "Six colours and three thicknesses. Works with a mouse, a finger or a tablet pen."),
         ("Sticky notes", "Double-tap for a note, type, and drag it where it belongs. The text shrinks to fit."),
         ("Shapes and arrows", "Rectangles, ellipses, triangles and diamonds. Arrows stay attached when you move things."),
         ("An endless board", "Pan and zoom with two fingers or the mouse wheel. One tap fits everything on screen."),
         ("Saved as you go", "Every board is saved in this browser automatically. Close the tab and come back later."),
         ("Export as PNG", "Save the whole board as an image for a slide, a document or a chat.")],
  steps_h="From blank page to shared picture",
  steps=[("Open a board", "No sign-up. The board opens straight away."),
         ("Draw, write and connect", "Sketch with markers, add notes and shapes, link them with arrows."),
         ("Export the image", "Download a PNG and send it wherever you need it.")],
  price_h="Free, with a Pro plan when you need more",
  free="Free", free_list=["Up to {n} boards", "Every drawing tool", "PNG export", "Ads on the site pages"],
  pro="Pro", pro_list=["Unlimited boards", "No ads anywhere on the site", "Sharper exports without the SiteWhiteboard mark", "Back up and restore your boards as a file"],
  buy="Get Pro", soon="Pro is not on sale yet.", active="Pro is active in this browser.",
  faq_h="Questions",
  faq=[("Do I need an account?", "No. Open a board and draw. There is nothing to sign up for or install."),
       ("Where are my boards saved?", "In your browser, on the device you are using. They are not uploaded to a server. If you clear your browser's site data, the boards are deleted, so export anything important."),
       ("Can several people draw on the same board at once?", "Not yet. A board lives on one device. To share your work, export it as a PNG and send the image."),
       ("Does it work on a phone or tablet?", "Yes. Draw with a finger or a pen, and use two fingers to move and zoom the board."),
       ("Is SiteWhiteboard really free?", "Yes. Ads on the site pages pay for it. The Pro plan removes the ads and adds unlimited boards, sharper exports and backups.")],
  about="About", privacy="Privacy", terms="Terms", rights="All rights reserved.",
  about_t="About SiteWhiteboard",
  about_b=["SiteWhiteboard is a simple online whiteboard. It opens in one click, it needs no account, and it keeps your boards in your own browser.",
           "We built it for quick sketches, lesson notes, brainstorms and diagrams, for the moments when opening a big design tool is too much.",
           "Questions, bugs or ideas? Write to us at"],
  privacy_t="Privacy policy", updated="Last updated:",
  privacy_s=[("What SiteWhiteboard stores", "Your boards, your language choice and, if you have Pro, your licence key are stored in your browser's local storage on your device. SiteWhiteboard has no user accounts and does not upload your boards to a server."),
             ("Advertising", "We show ads from Google AdSense on our pages. Google and its partners use cookies to show ads based on your visits to this site and other sites. You can turn off personalised ads in Google's Ads Settings (adssettings.google.com), and read how Google uses data at policies.google.com/technologies/partner-sites."),
             ("Payments", "Pro is sold through a third-party payment provider. That provider handles your payment details; we never see your card number. When you activate Pro, your licence key is sent to the provider to check that it is valid."),
             ("Server logs", "Our hosting provider may record technical data such as your IP address and browser type for security and to keep the site running."),
             ("Contact", "For any privacy question, write to us at")],
  terms_t="Terms of use",
  terms_s=[("Using SiteWhiteboard", "You may use SiteWhiteboard for personal and professional work. Do not use it to break the law or to harm the site or other people."),
           ("Your content", "What you draw is yours. Your boards stay in your browser, so we cannot see them and we cannot recover them if they are lost. Export or back up anything you need to keep."),
           ("Pro", "Pro is a paid plan sold through a third-party payment provider. The price and billing terms are shown at checkout. A licence key activates Pro in your browser."),
           ("No warranty", "SiteWhiteboard is provided as it is, without any warranty. We are not liable for lost boards or for any damage that results from using the site, to the extent the law allows."),
           ("Changes", "We may update the site and these terms. The date at the top shows the latest version."),
           ("Contact", "Questions about these terms? Write to us at")],
),
"fr": dict(
  name="Français", title="SiteWhiteboard – tableau blanc en ligne gratuit, sans inscription",
  desc="Un tableau blanc en ligne gratuit avec marqueurs, post-it, formes et flèches. Sans compte, sans installation. Vos tableaux restent dans votre navigateur.",
  nav_feat="Fonctionnalités", nav_price="Tarifs", nav_faq="Questions", open="Ouvrir un tableau",
  h1a="Ouvrez un tableau blanc et ", h1b="dessinez", h1c=".",
  lead="SiteWhiteboard est un tableau blanc en ligne gratuit avec marqueurs, post-it, formes et flèches. Sans compte, sans installation. Vos tableaux restent dans votre navigateur.",
  small="Gratuit. Fonctionne sur téléphone, tablette et ordinateur.", hint="Essayez ici. Dessinez dans ce cadre.", clear="Effacer", ad="Publicité",
  feat_h="Tout ce qu’il faut sur un tableau blanc",
  feats=[("Marqueurs et gomme", "Six couleurs et trois épaisseurs. Fonctionne à la souris, au doigt ou au stylet."),
         ("Post-it", "Touchez deux fois pour créer un post-it, écrivez, puis déplacez-le. Le texte s’adapte à la taille."),
         ("Formes et flèches", "Rectangles, ellipses, triangles et losanges. Les flèches restent attachées quand vous déplacez les éléments."),
         ("Un tableau sans limites", "Déplacez et zoomez avec deux doigts ou la molette. Un seul geste affiche tout à l’écran."),
         ("Enregistrement automatique", "Chaque tableau est enregistré dans ce navigateur. Fermez l’onglet et revenez plus tard."),
         ("Export en PNG", "Enregistrez tout le tableau en image pour une présentation, un document ou une discussion.")],
  steps_h="De la page blanche à l’image partagée",
  steps=[("Ouvrez un tableau", "Aucune inscription. Le tableau s’ouvre tout de suite."),
         ("Dessinez, écrivez, reliez", "Esquissez au marqueur, ajoutez des post-it et des formes, reliez-les par des flèches."),
         ("Exportez l’image", "Téléchargez un PNG et envoyez-le où vous voulez.")],
  price_h="Gratuit, avec une offre Pro si vous en voulez plus",
  free="Gratuit", free_list=["Jusqu’à {n} tableaux", "Tous les outils de dessin", "Export en PNG", "Publicités sur les pages du site"],
  pro="Pro", pro_list=["Tableaux illimités", "Aucune publicité sur le site", "Exports plus nets, sans la mention SiteWhiteboard", "Sauvegarde et restauration de vos tableaux dans un fichier"],
  buy="Obtenir Pro", soon="Pro n’est pas encore en vente.", active="Pro est actif dans ce navigateur.",
  faq_h="Questions",
  faq=[("Faut-il un compte ?", "Non. Ouvrez un tableau et dessinez. Il n’y a rien à créer ni à installer."),
       ("Où sont enregistrés mes tableaux ?", "Dans votre navigateur, sur l’appareil que vous utilisez. Ils ne sont pas envoyés sur un serveur. Si vous effacez les données du site dans votre navigateur, les tableaux sont supprimés : exportez ce qui compte."),
       ("Plusieurs personnes peuvent-elles dessiner sur le même tableau en même temps ?", "Pas encore. Un tableau vit sur un seul appareil. Pour partager votre travail, exportez-le en PNG et envoyez l’image."),
       ("Est-ce que ça marche sur téléphone ou tablette ?", "Oui. Dessinez au doigt ou au stylet, et utilisez deux doigts pour déplacer et zoomer."),
       ("SiteWhiteboard est-il vraiment gratuit ?", "Oui. Les publicités sur les pages du site le financent. L’offre Pro retire les publicités et ajoute les tableaux illimités, des exports plus nets et les sauvegardes.")],
  about="À propos", privacy="Confidentialité", terms="Conditions", rights="Tous droits réservés.",
  about_t="À propos de SiteWhiteboard",
  about_b=["SiteWhiteboard est un tableau blanc en ligne tout simple. Il s’ouvre en un clic, ne demande aucun compte et garde vos tableaux dans votre navigateur.",
           "Nous l’avons conçu pour les croquis rapides, les notes de cours, les remue-méninges et les schémas, quand ouvrir un gros logiciel de design est de trop.",
           "Une question, un bug ou une idée ? Écrivez-nous à"],
  privacy_t="Politique de confidentialité", updated="Dernière mise à jour :",
  privacy_s=[("Ce que SiteWhiteboard enregistre", "Vos tableaux, votre choix de langue et, si vous avez Pro, votre clé de licence sont enregistrés dans le stockage local de votre navigateur, sur votre appareil. SiteWhiteboard n’a pas de comptes utilisateurs et n’envoie pas vos tableaux sur un serveur."),
             ("Publicité", "Nous affichons des annonces Google AdSense sur nos pages. Google et ses partenaires utilisent des cookies pour diffuser des annonces en fonction de vos visites sur ce site et sur d’autres sites. Vous pouvez désactiver les annonces personnalisées dans les paramètres des annonces Google (adssettings.google.com) et lire comment Google utilise les données sur policies.google.com/technologies/partner-sites."),
             ("Paiements", "Pro est vendu par un prestataire de paiement tiers. Ce prestataire traite vos informations de paiement ; nous ne voyons jamais votre numéro de carte. Quand vous activez Pro, votre clé de licence est envoyée au prestataire pour vérifier qu’elle est valide."),
             ("Journaux du serveur", "Notre hébergeur peut enregistrer des données techniques comme votre adresse IP et votre type de navigateur, pour la sécurité et le bon fonctionnement du site."),
             ("Contact", "Pour toute question sur la confidentialité, écrivez-nous à")],
  terms_t="Conditions d’utilisation",
  terms_s=[("Utiliser SiteWhiteboard", "Vous pouvez utiliser SiteWhiteboard pour un usage personnel ou professionnel. Ne l’utilisez pas pour enfreindre la loi ni pour nuire au site ou à autrui."),
           ("Votre contenu", "Ce que vous dessinez vous appartient. Vos tableaux restent dans votre navigateur : nous ne pouvons ni les voir ni les récupérer s’ils sont perdus. Exportez ou sauvegardez ce que vous devez garder."),
           ("Pro", "Pro est une offre payante vendue par un prestataire de paiement tiers. Le prix et les conditions de facturation sont affichés au moment du paiement. Une clé de licence active Pro dans votre navigateur."),
           ("Absence de garantie", "SiteWhiteboard est fourni tel quel, sans aucune garantie. Nous ne sommes pas responsables des tableaux perdus ni des dommages liés à l’utilisation du site, dans les limites permises par la loi."),
           ("Modifications", "Nous pouvons mettre à jour le site et ces conditions. La date en haut indique la dernière version."),
           ("Contact", "Une question sur ces conditions ? Écrivez-nous à")],
),
"ar": dict(
  name="العربية", title="SiteWhiteboard – سبورة بيضاء مجانية على الإنترنت بدون تسجيل",
  desc="سبورة بيضاء مجانية على الإنترنت بأقلام وأوراق لاصقة وأشكال وأسهم. بدون حساب وبدون تثبيت. لوحاتك تبقى في متصفحك.",
  nav_feat="المزايا", nav_price="الأسعار", nav_faq="أسئلة", open="افتح لوحة",
  h1a="افتح سبورة بيضاء و", h1b="ابدأ الرسم", h1c=".",
  lead="SiteWhiteboard سبورة بيضاء مجانية على الإنترنت بأقلام وأوراق لاصقة وأشكال وأسهم. بدون حساب وبدون تثبيت. لوحاتك تبقى في متصفحك.",
  small="مجانية. تعمل على الهاتف والجهاز اللوحي والحاسوب.", hint="جرّب هنا. ارسم داخل هذا الإطار.", clear="مسح", ad="إعلان",
  feat_h="كل ما تحتاجه السبورة البيضاء",
  feats=[("أقلام وممحاة", "ستة ألوان وثلاث سماكات. تعمل بالفأرة أو الإصبع أو قلم الجهاز اللوحي."),
         ("أوراق لاصقة", "انقر مرتين لإضافة ورقة، اكتب، ثم اسحبها إلى مكانها. النص يتكيف مع حجم الورقة."),
         ("أشكال وأسهم", "مستطيلات وأشكال بيضاوية ومثلثات ومعيّنات. الأسهم تبقى متصلة عند تحريك العناصر."),
         ("لوحة بلا حدود", "حرّك وكبّر بإصبعين أو بعجلة الفأرة. نقرة واحدة تُظهر كل شيء على الشاشة."),
         ("حفظ تلقائي", "كل لوحة تُحفظ تلقائيًا في هذا المتصفح. أغلق الصفحة وعد لاحقًا."),
         ("تصدير بصيغة PNG", "احفظ اللوحة كاملة كصورة لعرض تقديمي أو مستند أو محادثة.")],
  steps_h="من صفحة فارغة إلى صورة جاهزة للمشاركة",
  steps=[("افتح لوحة", "بدون تسجيل. اللوحة تفتح فورًا."),
         ("ارسم واكتب واربط", "ارسم بالأقلام، أضف أوراقًا وأشكالًا، واربط بينها بالأسهم."),
         ("صدّر الصورة", "نزّل صورة PNG وأرسلها حيث تشاء.")],
  price_h="مجانية، مع خطة Pro عند الحاجة إلى المزيد",
  free="مجانية", free_list=["حتى {n} لوحات", "كل أدوات الرسم", "تصدير بصيغة PNG", "إعلانات في صفحات الموقع"],
  pro="Pro", pro_list=["لوحات غير محدودة", "بدون إعلانات في الموقع", "تصدير أوضح بدون علامة SiteWhiteboard", "نسخ احتياطي واستعادة للوحاتك في ملف"],
  buy="احصل على Pro", soon="Pro غير متاح للبيع بعد.", active="Pro مفعّل في هذا المتصفح.",
  faq_h="أسئلة",
  faq=[("هل أحتاج إلى حساب؟", "لا. افتح لوحة وابدأ الرسم. لا يوجد تسجيل ولا تثبيت."),
       ("أين تُحفظ لوحاتي؟", "في متصفحك، على الجهاز الذي تستخدمه. لا تُرفع إلى أي خادم. إذا مسحت بيانات الموقع من المتصفح ستُحذف اللوحات، لذلك صدّر ما يهمك."),
       ("هل يمكن لعدة أشخاص الرسم على اللوحة نفسها في الوقت نفسه؟", "ليس بعد. اللوحة موجودة على جهاز واحد. لمشاركة عملك، صدّره بصيغة PNG وأرسل الصورة."),
       ("هل تعمل على الهاتف أو الجهاز اللوحي؟", "نعم. ارسم بإصبعك أو بالقلم، واستخدم إصبعين لتحريك اللوحة وتكبيرها."),
       ("هل SiteWhiteboard مجانية فعلًا؟", "نعم. الإعلانات في صفحات الموقع تغطي تكلفتها. خطة Pro تزيل الإعلانات وتضيف لوحات غير محدودة وتصديرًا أوضح ونسخًا احتياطية.")],
  about="من نحن", privacy="الخصوصية", terms="الشروط", rights="جميع الحقوق محفوظة.",
  about_t="عن SiteWhiteboard",
  about_b=["SiteWhiteboard سبورة بيضاء بسيطة على الإنترنت. تفتح بنقرة واحدة، لا تحتاج إلى حساب، وتحفظ لوحاتك في متصفحك.",
           "صمّمناها للرسومات السريعة وملاحظات الدروس والعصف الذهني والمخططات، حين يكون فتح برنامج تصميم كبير أكثر من اللازم.",
           "سؤال أو خلل أو اقتراح؟ راسلنا على"],
  privacy_t="سياسة الخصوصية", updated="آخر تحديث:",
  privacy_s=[("ما الذي يحفظه SiteWhiteboard", "لوحاتك واختيارك للغة، ومفتاح الترخيص إن كانت لديك خطة Pro، تُحفظ في التخزين المحلي لمتصفحك على جهازك. لا توجد حسابات مستخدمين في SiteWhiteboard ولا تُرفع لوحاتك إلى أي خادم."),
             ("الإعلانات", "نعرض إعلانات Google AdSense في صفحاتنا. تستخدم Google وشركاؤها ملفات تعريف الارتباط لعرض الإعلانات بناءً على زياراتك لهذا الموقع ولمواقع أخرى. يمكنك إيقاف الإعلانات المخصصة من إعدادات إعلانات Google (adssettings.google.com)، ومعرفة كيف تستخدم Google البيانات على policies.google.com/technologies/partner-sites."),
             ("المدفوعات", "تُباع خطة Pro عبر مزوّد دفع خارجي. هذا المزوّد هو من يعالج بيانات الدفع، ونحن لا نرى رقم بطاقتك أبدًا. عند تفعيل Pro يُرسل مفتاح الترخيص إلى المزوّد للتحقق من صلاحيته."),
             ("سجلات الخادم", "قد يسجّل مزوّد الاستضافة بيانات تقنية مثل عنوان IP ونوع المتصفح لأغراض الأمان وضمان عمل الموقع."),
             ("التواصل", "لأي سؤال عن الخصوصية، راسلنا على")],
  terms_t="شروط الاستخدام",
  terms_s=[("استخدام SiteWhiteboard", "يمكنك استخدام SiteWhiteboard لأعمالك الشخصية والمهنية. لا تستخدمه لمخالفة القانون أو للإضرار بالموقع أو بالآخرين."),
           ("محتواك", "ما ترسمه ملك لك. لوحاتك تبقى في متصفحك، فلا نستطيع رؤيتها ولا استرجاعها إذا ضاعت. صدّر أو انسخ احتياطيًا ما تريد الاحتفاظ به."),
           ("Pro", "Pro خطة مدفوعة تُباع عبر مزوّد دفع خارجي. السعر وشروط الفوترة تظهر عند الدفع. مفتاح الترخيص يفعّل Pro في متصفحك."),
           ("إخلاء المسؤولية", "يُقدَّم SiteWhiteboard كما هو، بدون أي ضمان. لسنا مسؤولين عن ضياع اللوحات أو عن أي ضرر ناتج عن استخدام الموقع، في الحدود التي يسمح بها القانون."),
           ("التعديلات", "قد نحدّث الموقع وهذه الشروط. التاريخ في الأعلى يبيّن آخر نسخة."),
           ("التواصل", "أسئلة عن هذه الشروط؟ راسلنا على")],
),
}

EXTRA = {
"en": dict(short="EN", badge="Free · No sign-up · Nothing to install", more="See the features",
  notes=["Idea", "Plan", "To do"], uses_h="One board, many uses", cta_h="Ready to draw?",
  uses=[("Brainstorming", "Throw ideas on sticky notes, group them and see what stands out."),
        ("Teaching", "Explain a lesson with markers, the way you would on a classroom board."),
        ("Diagrams", "Draw flows and maps with shapes and arrows that stay connected."),
        ("Meetings", "Share your screen and sketch while you talk, then send the picture.")]),
"fr": dict(short="FR", badge="Gratuit · Sans inscription · Rien à installer", more="Voir les fonctionnalités",
  notes=["Idée", "Plan", "À faire"], uses_h="Un tableau, mille usages", cta_h="Prêt à dessiner ?",
  uses=[("Remue-méninges", "Notez vos idées sur des post-it, regroupez-les et voyez ce qui ressort."),
        ("Enseignement", "Expliquez un cours au marqueur, comme sur le tableau de la classe."),
        ("Schémas", "Dessinez des flux et des cartes avec des formes et des flèches qui restent reliées."),
        ("Réunions", "Partagez votre écran et dessinez en parlant, puis envoyez l’image.")]),
"ar": dict(short="عربي", badge="مجانية · بدون تسجيل · بدون تثبيت", more="اكتشف المزايا",
  notes=["فكرة", "خطة", "مهام"], uses_h="لوحة واحدة لاستخدامات كثيرة", cta_h="جاهز للرسم؟",
  uses=[("العصف الذهني", "دوّن أفكارك على أوراق لاصقة، اجمعها وانظر ما يبرز منها."),
        ("التدريس", "اشرح الدرس بالأقلام كما تفعل على سبورة القسم."),
        ("المخططات", "ارسم المسارات والخرائط بأشكال وأسهم تبقى متصلة."),
        ("الاجتماعات", "شارك شاشتك وارسم وأنت تتحدث، ثم أرسل الصورة.")]),
}
PAGE = {
"en": dict(brand="SiteWhiteboard", top="Back to top", product="Product", company="Company", contact="Contact", lang_label="Language",
  ab_eyebrow="About us", ab_lead="A whiteboard that opens in one click. No account, nothing to install, and your boards stay with you.",
  ab_vals=[("Free to use", "Every drawing tool is free. Ads on the site pages pay for it."),
           ("Private by design", "Boards are saved in your browser. They never go to our servers."),
           ("Ready in a second", "No sign-up and no download. Open a board and start drawing.")],
  ab_story_h="Why we built it",
  ab_story=["Big design tools are great for big projects. But most of the time you just need to sketch an idea, explain a lesson or draw a quick diagram.",
            "SiteWhiteboard is made for those moments: markers, sticky notes, shapes and arrows on an endless board, on your phone, tablet or computer."],
  ab_contact_h="Talk to us", ab_contact="Questions, bugs or ideas? We read every message."),
"fr": dict(brand="SiteTableauBlanc", top="Retour en haut", product="Produit", company="Société", contact="Contact", lang_label="Langue",
  ab_eyebrow="Qui sommes-nous", ab_lead="Un tableau blanc qui s’ouvre en un clic. Sans compte, sans installation, et vos tableaux restent chez vous.",
  ab_vals=[("Gratuit", "Tous les outils de dessin sont gratuits. Les publicités sur les pages du site le financent."),
           ("Privé par conception", "Les tableaux sont enregistrés dans votre navigateur. Ils ne vont jamais sur nos serveurs."),
           ("Prêt en une seconde", "Ni inscription ni téléchargement. Ouvrez un tableau et dessinez.")],
  ab_story_h="Pourquoi nous l’avons créé",
  ab_story=["Les gros logiciels de design sont parfaits pour les gros projets. Mais la plupart du temps, il suffit d’esquisser une idée, d’expliquer un cours ou de tracer un schéma rapide.",
            "SiteWhiteboard est fait pour ces moments-là : marqueurs, post-it, formes et flèches sur un tableau sans limites, sur téléphone, tablette ou ordinateur."],
  ab_contact_h="Écrivez-nous", ab_contact="Une question, un bug ou une idée ? Nous lisons tous les messages."),
"ar": dict(brand="موقع اللوحة البيضاء", top="العودة إلى الأعلى", product="المنتج", company="الشركة", contact="التواصل", lang_label="اللغة",
  ab_eyebrow="من نحن", ab_lead="سبورة بيضاء تفتح بنقرة واحدة. بدون حساب، بدون تثبيت، ولوحاتك تبقى معك.",
  ab_vals=[("مجانية", "كل أدوات الرسم مجانية. الإعلانات في صفحات الموقع تغطي التكلفة."),
           ("خصوصية من الأساس", "اللوحات تُحفظ في متصفحك ولا تصل أبدًا إلى خوادمنا."),
           ("جاهزة في ثانية", "بدون تسجيل وبدون تنزيل. افتح لوحة وابدأ الرسم.")],
  ab_story_h="لماذا صنعناها",
  ab_story=["برامج التصميم الكبيرة ممتازة للمشاريع الكبيرة. لكن في أغلب الأحيان تحتاج فقط إلى رسم فكرة أو شرح درس أو رسم مخطط سريع.",
            "SiteWhiteboard صُنعت لهذه اللحظات: أقلام وأوراق لاصقة وأشكال وأسهم على لوحة بلا حدود، على الهاتف أو الجهاز اللوحي أو الحاسوب."],
  ab_contact_h="تواصل معنا", ab_contact="سؤال أو خلل أو اقتراح؟ نقرأ كل الرسائل."),
}
# SEO wording. Target searches: "whiteboard online", "online whiteboard", "digital white board",
# "whiteboard app", "white board on screen", "white board for study", "white board for kids"
# (fr: "tableau blanc en ligne", "tableau blanc numérique"; ar: "سبورة بيضاء أونلاين", "سبورة إلكترونية").
SEO = {
"en": dict(
  title="Free Online Whiteboard, No Sign-up | SiteWhiteboard",
  desc="Free online whiteboard: a digital white board with markers, sticky notes and shapes for study, teaching, kids and meetings. No sign-up, no install.",
  h1a="A free online whiteboard to ", h1b="start drawing", h1c=".",
  feat_h="Everything you need in a digital whiteboard",
  uses_h="An online whiteboard for study, class and work",
  uses=[("Study", "Revise, solve problems and make mind maps on a white board for study, on your laptop or tablet."),
        ("Teaching", "Explain a lesson with markers, like on a classroom board, and share it on screen."),
        ("Kids", "A simple white board for kids: big colours, a finger to draw, nothing to install or sign up for."),
        ("Meetings", "Use it as a white board on screen: share your screen and sketch ideas while you talk.")],
  faq_more=[("What is an online whiteboard?", "An online whiteboard is a digital white board that opens in your web browser. You draw with a mouse, a finger or a pen, add sticky notes and shapes, and save the board as an image. SiteWhiteboard is free and needs no sign-up."),
            ("Can I use it as a whiteboard on screen or on a TV?", "Yes. Open the board on a computer connected to a projector, a TV or an interactive screen, or share your screen in a video call. Anyone watching sees what you draw."),
            ("Is it a good white board for kids and students?", "Yes. It has no account and no ads on the drawing screen, big colour markers, and works with a finger on a tablet. Students use it for study notes, maths and mind maps."),
            ("Do I need to download a whiteboard app?", "No. SiteWhiteboard works in the browser on Windows, Mac, Chromebook, Android, iPhone and iPad. Nothing to download or install.")],
  board_title="Online Whiteboard – Draw Now, Free | SiteWhiteboard",
  board_desc="Start drawing on a free online whiteboard: markers, sticky notes, shapes and arrows. No sign-up, works on phone, tablet and computer."),
"fr": dict(
  title="Tableau blanc en ligne gratuit, sans inscription | SiteWhiteboard",
  desc="Tableau blanc en ligne gratuit : un tableau numérique avec marqueurs, post-it et formes pour réviser, enseigner, les enfants et les réunions. Sans compte.",
  h1a="Un tableau blanc en ligne gratuit pour ", h1b="dessiner", h1c=".",
  feat_h="Tout ce qu’il faut dans un tableau blanc numérique",
  uses_h="Un tableau blanc en ligne pour réviser, enseigner et travailler",
  uses=[("Révisions", "Révisez, résolvez des exercices et faites des cartes mentales sur ordinateur ou tablette."),
        ("Enseignement", "Expliquez un cours au marqueur, comme au tableau de la classe, et partagez-le à l’écran."),
        ("Enfants", "Un tableau blanc simple pour les enfants : de grandes couleurs, on dessine au doigt, rien à installer."),
        ("Réunions", "Utilisez-le comme tableau blanc à l’écran : partagez votre écran et dessinez en parlant.")],
  faq_more=[("Qu’est-ce qu’un tableau blanc en ligne ?", "C’est un tableau blanc numérique qui s’ouvre dans le navigateur. Vous dessinez à la souris, au doigt ou au stylet, ajoutez des post-it et des formes, puis enregistrez le tableau en image. SiteWhiteboard est gratuit et sans inscription."),
            ("Puis-je l’utiliser sur un écran ou une télévision ?", "Oui. Ouvrez le tableau sur un ordinateur relié à un vidéoprojecteur, une télé ou un écran interactif, ou partagez votre écran en visio. Tout le monde voit ce que vous dessinez."),
            ("Est-ce adapté aux enfants et aux élèves ?", "Oui. Pas de compte, pas de publicité sur l’écran de dessin, de grands marqueurs de couleur, et on dessine au doigt sur tablette. Les élèves s’en servent pour les révisions, les maths et les cartes mentales."),
            ("Faut-il télécharger une application ?", "Non. SiteWhiteboard fonctionne dans le navigateur sur Windows, Mac, Chromebook, Android, iPhone et iPad. Rien à télécharger.")],
  board_title="Tableau blanc en ligne gratuit – Dessinez | SiteWhiteboard",
  board_desc="Dessinez sur un tableau blanc en ligne gratuit : marqueurs, post-it, formes et flèches. Sans inscription, sur téléphone, tablette et ordinateur."),
"ar": dict(
  title="سبورة بيضاء أونلاين مجانية بدون تسجيل | SiteWhiteboard",
  desc="سبورة بيضاء أونلاين مجانية تفتح بنقرة واحدة. سبورة إلكترونية بأقلام وأوراق لاصقة وأشكال وأسهم للمراجعة والتدريس والأطفال والاجتماعات. بدون حساب وبدون تثبيت.",
  h1a="سبورة بيضاء أونلاين مجانية لكي ", h1b="تبدأ الرسم", h1c=".",
  feat_h="كل ما تحتاجه في سبورة إلكترونية",
  uses_h="سبورة أونلاين للمراجعة والتدريس والعمل",
  uses=[("المراجعة", "راجع دروسك وحل التمارين وارسم الخرائط الذهنية على الحاسوب أو الجهاز اللوحي."),
        ("التدريس", "اشرح الدرس بالأقلام كما على سبورة القسم، واعرضه على الشاشة."),
        ("الأطفال", "سبورة بسيطة للأطفال: ألوان كبيرة، الرسم بالإصبع، وبدون تثبيت أو تسجيل."),
        ("الاجتماعات", "استعملها كسبورة على الشاشة: شارك شاشتك وارسم أفكارك وأنت تتحدث.")],
  faq_more=[("ما هي السبورة البيضاء الأونلاين؟", "هي سبورة إلكترونية تفتح في المتصفح. ترسم بالفأرة أو الإصبع أو القلم، تضيف أوراقًا لاصقة وأشكالًا، ثم تحفظ اللوحة كصورة. SiteWhiteboard مجانية وبدون تسجيل."),
            ("هل يمكن استعمالها على شاشة أو تلفاز؟", "نعم. افتح اللوحة على حاسوب متصل بجهاز عرض أو تلفاز أو شاشة تفاعلية، أو شارك شاشتك في مكالمة فيديو. الجميع يرى ما ترسمه."),
            ("هل هي مناسبة للأطفال والتلاميذ؟", "نعم. لا حساب ولا إعلانات في شاشة الرسم، أقلام ملونة كبيرة، والرسم بالإصبع على الجهاز اللوحي. يستعملها التلاميذ للمراجعة والرياضيات والخرائط الذهنية."),
            ("هل أحتاج إلى تنزيل تطبيق؟", "لا. SiteWhiteboard تعمل في المتصفح على Windows وMac وChromebook وAndroid وiPhone وiPad. لا شيء للتنزيل.")],
  board_title="سبورة بيضاء أونلاين – ارسم الآن مجانًا | SiteWhiteboard",
  board_desc="ارسم على سبورة بيضاء أونلاين مجانية: أقلام وأوراق لاصقة وأشكال وأسهم. بدون تسجيل، على الهاتف والجهاز اللوحي والحاسوب."),
}
LOCALE = {"en": "en_US", "fr": "fr_FR", "ar": "ar_MA"}
for _k in L:
    L[_k].update(EXTRA[_k])
    L[_k].update(PAGE[_k])
    _seo = dict(SEO[_k])
    L[_k]["faq"] = _seo.pop("faq_more") + L[_k]["faq"]
    L[_k].update(_seo)

CAPS = ["blue", "red", "green", "amber", "violet", "ink"]
PAPERS = ["amber", "green", "blue", "violet"]
FEAT_ICONS = ["M4 20l1-4L16 5l3 3L8 19zM14 7l3 3", "M5 5h14v9l-5 5H5zM14 19v-5h5", "M4 5h9v9H4zM13 20l7-7M15 13h5v5",
              "M12 3v18M3 12h18M9 6l3-3 3 3M9 18l3 3 3-3M6 9l-3 3 3 3M18 9l3 3-3 3", "M5 12.5l4.5 4.5L19 7", "M12 4v11M7 10l5 5 5-5M5 20h14"]
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
e = html.escape


def prefix(lang):
    return "" if lang == "en" else "/" + lang


def board(lang):
    """Clean address of the whiteboard: /board/, /fr/board/, /ar/board/"""
    return prefix(lang) + "/board/"


def url(lang, page):
    return prefix(lang) + ("/" if page == "index" else "/" + page + ".html")


def head(a, lang, page, title, desc):
    d = L[lang]
    alts = "".join(f'<link rel="alternate" hreflang="{x}" href="{a.domain}{url(x, page)}">' for x in LANGS)
    return f"""<!doctype html>
<html lang="{lang}" dir="{'rtl' if lang == 'ar' else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{a.domain}{url(lang, page)}">
{alts}<link rel="alternate" hreflang="x-default" href="{a.domain}{url('en', page)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#1f5fd1">
<meta property="og:site_name" content="SiteWhiteboard"><meta property="og:locale" content="{LOCALE[lang]}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{a.domain}{url(lang, page)}">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}">
<link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Readex+Pro:wght@400;600&family=Shantell+Sans:wght@500&display=swap">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="{url(lang, 'index')}"><i class="logo"></i>{e(d['brand'])}</a>
  <nav><a href="{url(lang, 'index')}#features">{e(d['nav_feat'])}</a><a href="{url(lang, 'index')}#pricing">{e(d['nav_price'])}</a><a href="{url(lang, 'index')}#faq">{e(d['nav_faq'])}</a></nav>
  {lang_toggle(lang, page)}
  <a class="cta small" href="{board(lang)}">{e(d['open'])}</a>
</div></header>
"""


def lang_toggle(lang, page):
    """Language switcher: a button showing the current language that opens a small menu."""
    items = "".join(
        f'<a href="{url(x, page)}" hreflang="{x}" lang="{x}"{" aria-current=" + chr(34) + "true" + chr(34) if x == lang else ""}>'
        f'{flag(x)}<span>{e(L[x]["name"])}</span><b>{e(L[x]["short"])}</b></a>' for x in LANGS)
    return (f'<details class="langdd"><summary aria-label="{e(L[lang]["lang_label"])}">'
            f'{flag(lang)}{e(L[lang]["short"])}'
            f'<svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 10l5 5 5-5"/></svg></summary>'
            f'<div class="menu">{items}</div></details>')


def foot(a, lang, page="index"):
    d = L[lang]
    home = url(lang, 'index')
    host = urlparse(a.domain).hostname or ""
    return f"""<footer><div class="wrap">
  <div class="fbrand"><a class="brand" href="{home}"><i class="logo"></i>{e(d['brand'])}</a><p>{e(d['small'])}</p>
    <a class="cta small" href="{board(lang)}">{e(d['open'])}</a></div>
  <nav class="fcol"><h4>{e(d['product'])}</h4><a href="{home}#features">{e(d['nav_feat'])}</a><a href="{home}#pricing">{e(d['nav_price'])}</a><a href="{home}#faq">{e(d['nav_faq'])}</a></nav>
  <nav class="fcol"><h4>{e(d['company'])}</h4><a href="{url(lang, 'about')}">{e(d['about'])}</a><a href="{url(lang, 'privacy')}">{e(d['privacy'])}</a><a href="{url(lang, 'terms')}">{e(d['terms'])}</a></nav>
  <div class="legal"><span>© 2026 {e(d['brand'])}. {e(d['rights'])}</span><span dir="ltr">{e(host)}</span></div>
</div></footer>
<a class="totop" id="totop" href="#" aria-label="{e(d['top'])}" title="{e(d['top'])}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M6 11l6-6 6 6"/></svg></a>
<script src="/assets/config.js"></script>
<script src="/assets/site.js"></script>
</body>
</html>
"""


def ad(lang, slot):
    return f'<div class="ad" data-ad="{slot}" data-label="{e(L[lang]["ad"])}"></div>\n'


def landing(a, lang):
    d = L[lang]
    feats = "".join(f'<li style="--c:var(--m-{CAPS[i]})"><span class="ic"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{FEAT_ICONS[i]}"/></svg></span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(d["feats"]))
    uses = "".join(f'<li style="background:var(--p-{PAPERS[i]})"><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(d["uses"]))
    notes = "".join(f'<span class="sticky s{i + 1}" aria-hidden="true">{e(t)}</span>' for i, t in enumerate(d["notes"]))
    host = urlparse(a.domain).hostname or "example.com"
    steps = "".join(f"<li><h3>{e(t)}</h3><p>{e(p)}</p></li>" for t, p in d["steps"])
    fl = "".join(f"<li>{e(x.replace('{n}', str(a.free)))}</li>" for x in d["free_list"])
    pl = "".join(f"<li>{e(x)}</li>" for x in d["pro_list"])
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(r)}</p></details>" for q, r in d["faq"])
    caps = "".join(f'<button class="cap" data-c="{c}" style="background:var(--m-{c})" aria-pressed="{"true" if c == "blue" else "false"}" aria-label="{c}"></button>' for c in CAPS)
    ld = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": a.domain + "/#site", "name": "SiteWhiteboard", "alternateName": d["brand"], "url": a.domain + "/", "inLanguage": LANGS},
        {"@type": "WebApplication", "name": "SiteWhiteboard", "url": a.domain + board(lang), "applicationCategory": "DesignApplication",
         "operatingSystem": "Windows, macOS, ChromeOS, Android, iOS", "browserRequirements": "Requires a modern web browser",
         "inLanguage": lang, "description": d["desc"], "isAccessibleForFree": True,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in d["faq"]]},
    ]}, ensure_ascii=False)
    return head(a, lang, "index", d["title"], d["desc"]) + f"""<main>
<div class="hero"><div class="wrap">
  <div class="copy">
  <span class="badge"><i></i>{e(d['badge'])}</span>
  <h1>{e(d['h1a'])}<span class="hand">{e(d['h1b'])}</span>{e(d['h1c'])}</h1>
  <p class="lead">{e(d['lead'])}</p>
  <div class="actions"><a class="cta big" href="{board(lang)}">{e(d['open'])}{ARROW}</a><a class="cta big ghost" href="#features">{e(d['more'])}</a></div>
  <small>{e(d['small'])}</small>
  </div>
  <div class="stage">
    {notes}
    <div class="demo">
      <div class="chrome"><i></i><i></i><i></i><span>{e(host)}/board</span></div>
      <div class="pad"><canvas id="demo" aria-label="{e(d['hint'])}"></canvas><span class="hint" id="hint">{e(d['hint'])}</span></div>
      <div class="tray">{caps}<button class="clear" id="demoClear">{e(d['clear'])}</button></div>
    </div>
  </div>
</div></div>
{ad(lang, 'top')}<section><div class="wrap">
  <h2>{e(d['uses_h'])}</h2>
  <ul class="uses">{uses}</ul>
</div></section>
<section id="features" class="band"><div class="wrap">
  <h2>{e(d['feat_h'])}</h2>
  <ul class="feats">{feats}</ul>
</div></section>
<section><div class="wrap">
  <h2>{e(d['steps_h'])}</h2>
  <ol class="steps">{steps}</ol>
  <a class="cta center" href="{board(lang)}">{e(d['open'])}{ARROW}</a>
</div></section>
{ad(lang, 'middle')}<section id="pricing" class="band"><div class="wrap">
  <h2>{e(d['price_h'])}</h2>
  <div class="plans">
    <div class="plan"><h3>{e(d['free'])}</h3><ul>{fl}</ul><a class="cta ghost" href="{board(lang)}">{e(d['open'])}</a></div>
    <div class="plan pro"><h3>{e(d['pro'])}</h3><span class="price" id="price"></span><ul>{pl}</ul>
      <a class="cta" id="buy" target="_blank" rel="noopener" hidden>{e(d['buy'])}</a><p id="soon" hidden>{e(d['soon'])}</p><p id="proActive" hidden>{e(d['active'])}</p></div>
  </div>
</div></section>
<section id="faq"><div class="wrap">
  <h2>{e(d['faq_h'])}</h2>
  <div class="faq">{faq}</div>
</div></section>
<section class="final"><div class="wrap"><div class="box">
  <h2>{e(d['cta_h'])}</h2>
  <a class="cta big" href="{board(lang)}">{e(d['open'])}{ARROW}</a>
  <small>{e(d['badge'])}</small>
</div></div></section>
{ad(lang, 'bottom')}</main>
<script type="application/ld+json">{ld}</script>
""" + foot(a, lang)


def mail(a):
    return f'<span data-email dir="ltr">{e(a.email)}</span>'


def doc(a, lang, page, title, body):
    d = L[lang]
    return head(a, lang, page, title + " – SiteWhiteboard", d["desc"]) + f'<main class="wrap doc">\n<h1>{e(title)}</h1>\n{body}</main>\n{ad(lang, "bottom")}' + foot(a, lang, page)


def sections(a, lang, items):
    d = L[lang]
    out = f'<p class="note">{e(d["updated"])} {UPDATED[lang]}</p>\n'
    for i, (h, p) in enumerate(items):
        tail = " " + mail(a) + "." if i == len(items) - 1 else ""
        out += f"<h2>{e(h)}</h2>\n<p>{e(p)}{tail}</p>\n"
    return out


FLAGS = {'en': '<svg viewBox="0 0 60 30" preserveAspectRatio="xMidYMid slice"><rect width="60" height="30" fill="#012169"/><path d="M0 0L60 30M60 0L0 30" stroke="#fff" stroke-width="6"/><path d="M0 0L60 30M60 0L0 30" stroke="#C8102E" stroke-width="2"/><path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/><path d="M30 0v30M0 15h60" stroke="#C8102E" stroke-width="6"/></svg>', 'fr': '<svg viewBox="0 0 3 2" preserveAspectRatio="none"><rect width="1" height="2" fill="#0055A4"/><rect x="1" width="1" height="2" fill="#fff"/><rect x="2" width="1" height="2" fill="#EF4135"/></svg>', 'ar': '<svg viewBox="0 0 30 20" preserveAspectRatio="xMidYMid slice"><rect width="30" height="20" fill="#C1272D"/><path d="M15 5L17.94 14.05L10.24 8.45H19.76L12.06 14.05Z" fill="none" stroke="#006233" stroke-width="1.1" stroke-linejoin="round"/></svg>'}


def flag(lang):
    return f'<i class="flag" aria-hidden="true">{FLAGS[lang]}</i>'


VAL_ICONS = ['M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.4 6.7 19.4l1.2-6L3.4 9.3l6-.7z', 'M6 11V8a6 6 0 0112 0v3M5 11h14v10H5zM12 15v2', 'M13 3L5 14h6l-1 7 8-11h-6z']
VAL_COLORS = ["amber", "green", "blue"]


def about(a, lang):
    d = L[lang]
    vals = "".join(f'<li style="--c:var(--m-{VAL_COLORS[i]})"><span class="ic"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{VAL_ICONS[i]}"/></svg></span><h3>{e(t)}</h3><p>{e(p)}</p></li>'
                   for i, (t, p) in enumerate(d["ab_vals"]))
    story = "".join(f"<p>{e(p)}</p>" for p in d["ab_story"])
    notes = "".join(f'<span class="note n{i + 1}" style="background:var(--p-{c})">{e(t)}</span>' for i, (t, c) in enumerate(zip(d["notes"], ["amber", "green", "violet"])))
    body = f"""<main class="about">
<section class="ab-hero"><div class="wrap">
  <span class="badge"><i></i>{e(d['ab_eyebrow'])}</span>
  <h1>{e(d['about_t'])}</h1>
  <p class="lead">{e(d['ab_lead'])}</p>
  <ul class="vals">{vals}</ul>
</div></section>
<section class="ab-story band"><div class="wrap">
  <div class="txt"><h2>{e(d['ab_story_h'])}</h2>{story}</div>
  <div class="board" aria-hidden="true">{notes}<svg class="arr" viewBox="0 0 200 80"><path d="M10 60C60 10 120 10 185 40M170 28l15 12-18 6"/></svg></div>
</div></section>
<section class="ab-cta"><div class="wrap"><div class="box">
  <h2>{e(d['cta_h'])}</h2>
  <p>{e(d['badge'])}</p>
  <div class="actions"><a class="cta big" href="{board(lang)}">{e(d['open'])}{ARROW}</a></div>
</div></div></section>
</main>
{ad(lang, "bottom")}"""
    return head(a, lang, "about", d["about_t"] + " – SiteWhiteboard", d["desc"]) + body + foot(a, lang, "about")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", default="https://www.sitewhiteboard.com", help="site address, no trailing slash")
    ap.add_argument("--adsense", default="", help="AdSense publisher id, e.g. ca-pub-1234567890123456")
    ap.add_argument("--slot-top", default=""); ap.add_argument("--slot-middle", default=""); ap.add_argument("--slot-bottom", default="")
    ap.add_argument("--email", default="")
    ap.add_argument("--checkout", default="", help="payment page for Pro")
    ap.add_argument("--validate", default="", help="licence check endpoint (POST license_key, answers JSON with valid:true)")
    ap.add_argument("--price", default="")
    ap.add_argument("--free", type=int, default=3, help="boards on the free plan")
    a = ap.parse_args()
    a.domain = a.domain.rstrip("/")
    if not a.email:
        a.email = "contact@" + re.sub(r"^www\.", "", urlparse(a.domain).hostname or "example.com")

    # empty dist/ without removing the folder itself: a preview server or terminal may be holding it open
    DIST.mkdir(exist_ok=True)
    for child in DIST.iterdir():
        shutil.rmtree(child) if child.is_dir() else child.unlink()
    (DIST / "assets").mkdir(parents=True)
    tokens = (SRC / "tokens.css").read_text(encoding="utf8")
    (DIST / "assets/site.css").write_text(tokens + (SRC / "site.body.css").read_text(encoding="utf8"), encoding="utf8")
    (DIST / "assets/app.css").write_text(tokens + (SRC / "app.body.css").read_text(encoding="utf8"), encoding="utf8")
    for f in ("app.js", "site.js", "icon.svg"):
        shutil.copy(SRC / f, DIST / "assets" / f)
    cfg = {"adsenseClient": a.adsense, "adSlots": {"top": a.slot_top, "middle": a.slot_middle, "bottom": a.slot_bottom},
           "proCheckoutUrl": a.checkout, "licenseValidateUrl": a.validate, "proPrice": a.price,
           "freeBoardLimit": a.free, "contactEmail": a.email}
    (DIST / "assets/config.js").write_text("window.FELT_CONFIG=" + json.dumps(cfg, ensure_ascii=False, indent=2) + ";\n", encoding="utf8")
    app = (SRC / "app.html").read_text(encoding="utf8")
    for lang in LANGS:
        page = (app.replace('<html lang="en">', f'<html lang="{lang}" dir="{"rtl" if lang == "ar" else "ltr"}">')
                   .replace("[[canonical]]", a.domain + board(lang))
                   .replace("[[title]]", e(L[lang]["board_title"])).replace("[[desc]]", e(L[lang]["board_desc"]))
                   .replace("[[alternates]]", "".join(f'<link rel="alternate" hreflang="{x}" href="{a.domain}{board(x)}">' for x in LANGS)))
        (DIST / board(lang).strip("/")).mkdir(parents=True, exist_ok=True)
        (DIST / board(lang).strip("/") / "index.html").write_text(page, encoding="utf8")
    # old address /app/?lang=xx keeps working: it forwards to the new one
    (DIST / "app").mkdir()
    (DIST / "app/index.html").write_text("""<!doctype html><html><head><meta charset="utf-8"><meta name="robots" content="noindex">
<link rel="canonical" href="%s/board/"><meta http-equiv="refresh" content="0;url=/board/">
<script>var l=new URLSearchParams(location.search).get('lang');location.replace((l==='fr'||l==='ar'?'/'+l:'')+'/board/'+location.hash)</script>
</head><body></body></html>
""" % a.domain, encoding="utf8")

    urls = [a.domain + board(x) for x in LANGS]
    for lang in LANGS:
        d = L[lang]
        base = DIST / lang if lang != "en" else DIST
        base.mkdir(exist_ok=True)
        pages = {"index": landing(a, lang), "about": about(a, lang),
                 "privacy": doc(a, lang, "privacy", d["privacy_t"], sections(a, lang, d["privacy_s"])),
                 "terms": doc(a, lang, "terms", d["terms_t"], sections(a, lang, d["terms_s"]))}
        for name, text in pages.items():
            (base / (name + ".html")).write_text(text, encoding="utf8")
            urls.append(a.domain + url(lang, name))
    today = datetime.date.today().isoformat()
    groups = [[board(x) for x in LANGS]] + [[url(x, p) for x in LANGS] for p in ("index", "about", "privacy", "terms")]
    prio = {"index": "1.0", "board": "0.9", "about": "0.5", "privacy": "0.3", "terms": "0.3"}
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for g in groups:
        kind = "board" if g[0].endswith("/board/") else ("index" if g[0] == "/" else g[0].strip("/").split(".")[0])
        links = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{x}" href="{a.domain}{g[n]}"/>' for n, x in enumerate(LANGS))
        links += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{a.domain}{g[0]}"/>'
        for u in g:
            out.append(f"  <url>\n    <loc>{a.domain}{u}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>{prio[kind]}</priority>{links}\n  </url>")
    out.append("</urlset>")
    (DIST / "sitemap.xml").write_text("\n".join(out) + "\n", encoding="utf8")
    (DIST / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n"
        "# /app/ only forwards old links to /board/\nDisallow: /app/\n\n"
        f"Sitemap: {a.domain}/sitemap.xml\n", encoding="utf8")
    if a.adsense:
        (DIST / "ads.txt").write_text(f"google.com, {a.adsense.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n", encoding="utf8")
    # version the css/js links so browsers never mix new pages with an old cached stylesheet
    import hashlib
    ver = hashlib.md5(b"".join(p.read_bytes() for p in sorted((DIST / "assets").iterdir()))).hexdigest()[:8]
    for p in DIST.rglob("*.html"):
        p.write_text(re.sub(r'(/assets/[\w.]+\.(?:css|js))"', r'\1?v=' + ver + '"', p.read_text(encoding="utf8")), encoding="utf8")
    print("Built", len(urls), "pages into", DIST)


if __name__ == "__main__":
    main()
