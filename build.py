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
UPDATED = {"en": "20 November 2026", "fr": "20 novembre 2026", "ar": "20 نوفمبر 2026"}
BLOG_DIR = ROOT / "content" / "blog"

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
             ("Cookies", "SiteWhiteboard itself does not set tracking cookies. When ads are shown, Google and its advertising partners may place and read cookies, or use web beacons and similar technologies, to serve and measure ads. Google's use of advertising cookies lets it and its partners show ads based on your visits to this site and other sites on the internet. You can block or delete cookies in your browser settings, and you can opt out of some third-party vendors' personalised ads at aboutads.info/choices."),
             ("Contact form", "The contact form does not send anything to our servers. It opens your own email app with your message filled in, and you decide whether to send it. When you write to us, we use your email address only to reply."),
             ("Children", "SiteWhiteboard has no accounts and does not knowingly collect personal information from children. Parents and teachers can let children draw without giving any personal details."),
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
             ("Cookies", "SiteWhiteboard ne dépose pas lui-même de cookies de suivi. Quand des annonces sont affichées, Google et ses partenaires publicitaires peuvent déposer et lire des cookies, ou utiliser des balises web et des technologies similaires, pour diffuser et mesurer les annonces. Les cookies publicitaires de Google lui permettent, ainsi qu’à ses partenaires, d’afficher des annonces en fonction de vos visites sur ce site et sur d’autres sites. Vous pouvez bloquer ou supprimer les cookies dans les réglages de votre navigateur, et refuser certaines annonces personnalisées de fournisseurs tiers sur youronlinechoices.eu."),
             ("Formulaire de contact", "Le formulaire de contact n’envoie rien à nos serveurs. Il ouvre votre propre messagerie avec votre message déjà rempli, et c’est vous qui décidez de l’envoyer. Quand vous nous écrivez, nous utilisons votre adresse uniquement pour vous répondre."),
             ("Enfants", "SiteWhiteboard n’a pas de comptes et ne collecte pas sciemment de données personnelles d’enfants. Parents et enseignants peuvent laisser les enfants dessiner sans donner aucune information personnelle."),
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
             ("ملفات تعريف الارتباط (الكوكيز)", "لا يضع SiteWhiteboard بنفسه ملفات تتبّع. عند عرض الإعلانات، قد تضع Google وشركاؤها الإعلانيون ملفات تعريف الارتباط وتقرؤها، أو تستخدم إشارات الويب وتقنيات مشابهة، لعرض الإعلانات وقياسها. تتيح ملفات Google الإعلانية لها ولشركائها عرض إعلانات بناءً على زياراتك لهذا الموقع ولمواقع أخرى. يمكنك حظر هذه الملفات أو حذفها من إعدادات متصفحك، ورفض بعض الإعلانات المخصصة من مزوّدين خارجيين عبر aboutads.info/choices."),
             ("نموذج التواصل", "نموذج التواصل لا يرسل أي شيء إلى خوادمنا. هو يفتح تطبيق البريد لديك ورسالتك مكتوبة فيه، وأنت من يقرر إرسالها. عندما تراسلنا نستعمل بريدك الإلكتروني فقط للرد عليك."),
             ("الأطفال", "لا توجد حسابات في SiteWhiteboard ولا نجمع عن قصد أي بيانات شخصية من الأطفال. يمكن للآباء والمعلمين ترك الأطفال يرسمون دون تقديم أي معلومات شخصية."),
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
# Home page explainer (shown under the live demo), contact page and blog labels
MORE = {
"en": dict(
  what_h="What is an online whiteboard?",
  what=["An online whiteboard is a drawing surface that opens in your web browser. It works like the whiteboard on a classroom or office wall, except the board never runs out of space and nothing needs wiping. You draw with a mouse, a finger or a stylus, write on sticky notes, add shapes and connect them with arrows. SiteWhiteboard saves every board in your browser while you work, so you can close the tab and pick up where you stopped.",
        "There is nothing to install and no account to create. Open a board, pick a marker colour and start. Two fingers or the mouse wheel move and zoom the board, and undo takes back any mistake. When the board is done, export it as a PNG image and put it in a slide, a document or a chat. You can also insert photos, screenshots or an earlier board and keep building on it.",
        "Your boards stay on your own device and are never uploaded to our servers. The flip side is that a board lives on one device: to share it, you export the picture."],
  who_h="Who uses it",
  who=[("Teachers", "Explain a lesson step by step on a projector or a shared screen, the way you would at the front of the room, then send the finished board to the class as a picture."),
       ("Students", "Revise with mind maps, work through maths problems by hand and keep a board for each subject on a laptop or tablet."),
       ("Companies", "Sketch a process during a video call, sort workshop ideas on sticky notes and turn a messy discussion into a diagram everyone can read.")],
  contact_t="Contact us", contact_lead="Questions, bug reports or ideas for the whiteboard? Send us a message. We read every one.",
  f_name="Your name", f_email="Your email", f_topic="Topic", f_topics=["A question", "A bug", "An idea", "Something else"],
  f_msg="Message", f_send="Open in my email app",
  f_note="This button opens your email app with the message filled in. If nothing opens, write to us directly at",
  tips_h="Before you write",
  tips=[("Reporting a bug?", "Tell us your device and browser (for example iPhone with Safari, or Android with Chrome) and what you did just before the problem."),
        ("Lost a board?", "Boards are saved in your browser, so we cannot see or recover them. Check that you are on the same device and the same browser you drew on."),
        ("Have an idea?", "Tell us what you were trying to do. A short example helps us more than a feature name.")],
  blog="Blog", blog_t="Whiteboard ideas, guides and lessons",
  blog_lead="Practical guides for teaching, studying, brainstorming and planning on an online whiteboard.",
  blog_desc="Guides and ideas for using an online whiteboard: teaching, maths, brainstorming, study, mind maps, flowcharts and comparisons of free whiteboard tools.",
  read="min read", related="Keep reading", try_h="Try it on a board", try_p="Open a free whiteboard and put this guide into practice. No sign-up.",
  all_posts="All articles"),
"fr": dict(
  what_h="Qu’est-ce qu’un tableau blanc en ligne ?",
  what=["Un tableau blanc en ligne est une surface de dessin qui s’ouvre dans votre navigateur. Il fonctionne comme le tableau blanc d’une salle de classe ou d’un bureau, sauf que la place ne manque jamais et qu’il n’y a rien à effacer à l’éponge. Vous dessinez à la souris, au doigt ou au stylet, écrivez sur des post-it, ajoutez des formes et les reliez par des flèches. SiteWhiteboard enregistre chaque tableau dans votre navigateur pendant que vous travaillez : vous pouvez fermer l’onglet et reprendre plus tard.",
        "Il n’y a rien à installer et aucun compte à créer. Ouvrez un tableau, choisissez une couleur de marqueur et commencez. Deux doigts ou la molette déplacent et zooment le tableau, et le bouton annuler rattrape toute erreur. Une fois terminé, exportez le tableau en image PNG pour une présentation, un document ou une discussion. Vous pouvez aussi insérer des photos, des captures d’écran ou un ancien tableau pour continuer dessus.",
        "Vos tableaux restent sur votre appareil et ne sont jamais envoyés sur nos serveurs. En contrepartie, un tableau vit sur un seul appareil : pour le partager, vous exportez l’image."],
  who_h="Qui l’utilise",
  who=[("Enseignants", "Expliquez un cours pas à pas sur un vidéoprojecteur ou un écran partagé, comme au tableau de la classe, puis envoyez le tableau terminé aux élèves en image."),
       ("Élèves et étudiants", "Révisez avec des cartes mentales, résolvez des exercices de maths à la main et gardez un tableau par matière sur ordinateur ou tablette."),
       ("Entreprises", "Esquissez un processus pendant une visio, triez les idées d’un atelier sur des post-it et transformez une discussion confuse en schéma lisible par tous.")],
  contact_t="Nous contacter", contact_lead="Une question, un bug ou une idée pour le tableau blanc ? Envoyez-nous un message. Nous les lisons tous.",
  f_name="Votre nom", f_email="Votre e-mail", f_topic="Sujet", f_topics=["Une question", "Un bug", "Une idée", "Autre chose"],
  f_msg="Message", f_send="Ouvrir dans ma messagerie",
  f_note="Ce bouton ouvre votre messagerie avec le message déjà rempli. Si rien ne s’ouvre, écrivez-nous directement à",
  tips_h="Avant d’écrire",
  tips=[("Un bug ?", "Indiquez votre appareil et votre navigateur (par exemple iPhone avec Safari, ou Android avec Chrome) et ce que vous faisiez juste avant le problème."),
        ("Un tableau perdu ?", "Les tableaux sont enregistrés dans votre navigateur : nous ne pouvons ni les voir ni les récupérer. Vérifiez que vous êtes sur le même appareil et le même navigateur."),
        ("Une idée ?", "Dites-nous ce que vous essayiez de faire. Un exemple concret nous aide plus qu’un nom de fonction.")],
  blog="Blog", blog_t="Idées, guides et cours pour le tableau blanc",
  blog_lead="Des guides pratiques (en anglais) pour enseigner, réviser, faire un remue-méninges et planifier sur un tableau blanc en ligne.",
  blog_desc="Guides et idées pour utiliser un tableau blanc en ligne.",
  read="min", related="À lire aussi", try_h="Essayez sur un tableau", try_p="Ouvrez un tableau blanc gratuit et mettez ce guide en pratique.",
  all_posts="Tous les articles"),
"ar": dict(
  what_h="ما هي السبورة البيضاء الأونلاين؟",
  what=["السبورة البيضاء الأونلاين مساحة للرسم تفتح في متصفح الإنترنت. تعمل مثل السبورة المعلّقة في القسم أو المكتب، لكن مساحتها لا تنتهي ولا تحتاج إلى مسح. ترسم بالفأرة أو بإصبعك أو بالقلم، تكتب على أوراق لاصقة، تضيف أشكالًا وتربط بينها بالأسهم. يحفظ SiteWhiteboard كل لوحة في متصفحك أثناء العمل، فيمكنك إغلاق الصفحة والعودة لاحقًا من حيث توقفت.",
        "لا يوجد ما تثبّته ولا حساب تنشئه. افتح لوحة، اختر لون القلم وابدأ. إصبعان أو عجلة الفأرة يحرّكان اللوحة ويكبّرانها، وزر التراجع يصحّح أي خطأ. عندما تنتهي، صدّر اللوحة كصورة PNG وضعها في عرض تقديمي أو مستند أو محادثة. ويمكنك أيضًا إدراج صور أو لقطات شاشة أو لوحة سابقة ومواصلة العمل عليها.",
        "لوحاتك تبقى على جهازك ولا تُرفع أبدًا إلى خوادمنا. في المقابل، اللوحة موجودة على جهاز واحد: لمشاركتها تصدّر الصورة."],
  who_h="من يستعملها",
  who=[("المعلمون", "اشرح الدرس خطوة بخطوة على جهاز العرض أو شاشة مشتركة كما تفعل أمام القسم، ثم أرسل اللوحة النهائية للتلاميذ كصورة."),
       ("التلاميذ والطلبة", "راجع بالخرائط الذهنية، حل تمارين الرياضيات بخط يدك، واحتفظ بلوحة لكل مادة على الحاسوب أو الجهاز اللوحي."),
       ("الشركات", "ارسم مسار عمل أثناء مكالمة فيديو، رتّب أفكار الورشة على أوراق لاصقة، وحوّل نقاشًا متشعبًا إلى مخطط واضح للجميع.")],
  contact_t="اتصل بنا", contact_lead="سؤال أو خلل أو فكرة للسبورة؟ أرسل لنا رسالة. نقرأ كل الرسائل.",
  f_name="اسمك", f_email="بريدك الإلكتروني", f_topic="الموضوع", f_topics=["سؤال", "خلل", "فكرة", "موضوع آخر"],
  f_msg="الرسالة", f_send="افتح في تطبيق البريد",
  f_note="هذا الزر يفتح تطبيق البريد لديك والرسالة مكتوبة فيه. إذا لم يُفتح شيء، راسلنا مباشرة على",
  tips_h="قبل أن تكتب",
  tips=[("تبلّغ عن خلل؟", "اذكر جهازك ومتصفحك (مثلًا iPhone مع Safari أو Android مع Chrome) وما فعلته قبل ظهور المشكلة مباشرة."),
        ("ضاعت لوحة؟", "اللوحات محفوظة في متصفحك، لذلك لا نستطيع رؤيتها ولا استرجاعها. تأكد أنك على الجهاز والمتصفح نفسيهما."),
        ("لديك فكرة؟", "أخبرنا بما كنت تحاول فعله. مثال قصير يفيدنا أكثر من اسم ميزة.")],
  blog="المدونة", blog_t="أفكار وأدلة ودروس للسبورة البيضاء",
  blog_lead="أدلة عملية (بالإنجليزية) للتدريس والمراجعة والعصف الذهني والتخطيط على سبورة أونلاين.",
  blog_desc="أدلة وأفكار لاستعمال السبورة البيضاء الأونلاين.",
  read="دقائق", related="اقرأ أيضًا", try_h="جرّب على لوحة", try_p="افتح سبورة مجانية وطبّق هذا الدليل.",
  all_posts="كل المقالات"),
}
LOCALE = {"en": "en_US", "fr": "fr_FR", "ar": "ar_MA"}
for _k in L:
    L[_k].update(EXTRA[_k])
    L[_k].update(PAGE[_k])
    L[_k].update(MORE[_k])
    _seo = dict(SEO[_k])
    L[_k]["faq"] = _seo.pop("faq_more") + L[_k]["faq"]
    L[_k].update(_seo)

CAPS = ["blue", "red", "green", "amber", "violet", "ink"]
PAPERS = ["amber", "green", "blue", "violet"]
FEAT_ICONS = ["M4 20l1-4L16 5l3 3L8 19zM14 7l3 3", "M5 5h14v9l-5 5H5zM14 19v-5h5", "M4 5h9v9H4zM13 20l7-7M15 13h5v5",
              "M12 3v18M3 12h18M9 6l3-3 3 3M9 18l3 3 3-3M6 9l-3 3 3 3M18 9l3 3-3 3", "M5 12.5l4.5 4.5L19 7", "M12 4v11M7 10l5 5 5-5M5 20h14"]
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
e = html.escape


SITE_CSS = ""


def minify_css(css):
    """Small, safe CSS squeeze: drop comments and extra spaces."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    return css.replace(";}", "}").strip()


def prefix(lang):
    return "" if lang == "en" else "/" + lang


def board(lang):
    """Clean address of the whiteboard: /board/, /fr/board/, /ar/board/"""
    return prefix(lang) + "/board/"


def url(lang, page):
    return prefix(lang) + ("/" if page == "index" else "/" + page + ".html")


def head(a, lang, page, title, desc, path=None, og="website", extra=""):
    """path: canonical path for pages that exist in one language only (the blog); they get no hreflang links
    and their language menu leads to each language's home page."""
    d = L[lang]
    canon = path or url(lang, page)
    if path:
        alts = ""
    else:
        alts = "".join(f'<link rel="alternate" hreflang="{x}" href="{a.domain}{url(x, page)}">' for x in LANGS)
        alts += f'<link rel="alternate" hreflang="x-default" href="{a.domain}{url("en", page)}">\n'
    return f"""<!doctype html>
<html lang="{lang}" dir="{'rtl' if lang == 'ar' else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{a.domain}{canon}">
{alts}<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#1f5fd1">
<meta property="og:site_name" content="SiteWhiteboard"><meta property="og:locale" content="{LOCALE[lang]}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="{og}"><meta property="og:url" content="{a.domain}{canon}">{extra}
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}">
<link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Readex+Pro:wght@400;600&family=Shantell+Sans:wght@500&display=swap" onload="this.onload=null;this.rel='stylesheet'"><noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Readex+Pro:wght@400;600&family=Shantell+Sans:wght@500&display=swap"></noscript>
<style>{SITE_CSS}</style>
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="{url(lang, 'index')}"><i class="logo"></i>{e(d['brand'])}</a>
  <nav><a href="{url(lang, 'index')}#features">{e(d['nav_feat'])}</a><a href="{url(lang, 'index')}#pricing">{e(d['nav_price'])}</a><a href="{url(lang, 'index')}#faq">{e(d['nav_faq'])}</a><a href="/blog/"{' aria-current="page"' if page == 'blog' else ''}>{e(d['blog'])}</a></nav>
  {lang_toggle(lang, 'index' if path else page)}
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
  <nav class="fcol"><h2 class="fh">{e(d['product'])}</h2><a href="{home}#features">{e(d['nav_feat'])}</a><a href="{home}#pricing">{e(d['nav_price'])}</a><a href="{home}#faq">{e(d['nav_faq'])}</a><a href="/blog/">{e(d['blog'])}</a></nav>
  <nav class="fcol"><h2 class="fh">{e(d['company'])}</h2><a href="{url(lang, 'about')}">{e(d['about'])}</a><a href="{url(lang, 'contact')}">{e(d['contact'])}</a><a href="{url(lang, 'privacy')}">{e(d['privacy'])}</a><a href="{url(lang, 'terms')}">{e(d['terms'])}</a></nav>
  <div class="legal"><span>© 2026 {e(d['brand'])}. {e(d['rights'])}</span><span dir="ltr">{e(host)}</span></div>
</div></footer>
<a class="totop" id="totop" href="#" aria-label="{e(d['top'])}" title="{e(d['top'])}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M6 11l6-6 6 6"/></svg></a>
<script src="/assets/config.js" defer></script>
<script src="/assets/site.js" defer></script>
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
    what = "".join(f"<p>{e(p)}</p>" for p in d["what"])
    who = "".join(f'<li style="--c:var(--m-{c})"><h3>{e(t)}</h3><p>{e(p)}</p></li>' for (t, p), c in zip(d["who"], ["blue", "green", "amber"]))
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
<section class="what band" id="what"><div class="wrap">
  <div class="txt"><h2>{e(d['what_h'])}</h2>{what}</div>
  <div class="who"><h3 class="who-h">{e(d['who_h'])}</h3><ul>{who}</ul></div>
</div></section>
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


def contact(a, lang):
    d = L[lang]
    opts = "".join(f"<option>{e(t)}</option>" for t in d["f_topics"])
    tips = "".join(f'<li style="--c:var(--m-{c})"><h3>{e(t)}</h3><p>{e(p)}</p></li>' for (t, p), c in zip(d["tips"], ["red", "blue", "amber"]))
    body = f"""<main class="contact"><div class="wrap">
<div class="c-intro">
  <span class="badge"><i></i>{e(d['contact'])}</span>
  <h1>{e(d['contact_t'])}</h1>
  <p class="lead">{e(d['contact_lead'])}</p>
  <h2 class="tips-h">{e(d['tips_h'])}</h2>
  <ul class="tips">{tips}</ul>
</div>
<form class="cform" id="cform" data-to="{e(a.email)}" novalidate>
  <label>{e(d['f_name'])}<input name="name" autocomplete="name" required maxlength="100"></label>
  <label>{e(d['f_email'])}<input name="email" type="email" autocomplete="email" required maxlength="200" dir="ltr"></label>
  <label>{e(d['f_topic'])}<select name="topic">{opts}</select></label>
  <label>{e(d['f_msg'])}<textarea name="message" rows="7" required maxlength="4000"></textarea></label>
  <button class="cta" type="submit">{e(d['f_send'])}{ARROW}</button>
  <p class="fnote">{e(d['f_note'])} <a data-mailto href="mailto:{e(a.email)}">{mail(a)}</a>.</p>
</form>
</div></main>
"""
    return head(a, lang, "contact", d["contact_t"] + " – SiteWhiteboard", d["contact_lead"]) + body + foot(a, lang, "contact")


# ---------- blog: Markdown files in content/blog/ become pages under /blog/ ----------
CAT_COLOR = {"Teaching": "blue", "Brainstorming": "amber", "Study": "green", "Guides": "violet", "Comparisons": "red", "Work": "ink"}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def md_inline(s):
    s = e(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)

    def link(m):
        href = m.group(2)
        ext = ' rel="noopener" target="_blank"' if href.startswith("http") else ""
        return f'<a href="{href}"{ext}>{m.group(1)}</a>'
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)


def md(text):
    """The small part of Markdown the articles use: ## headings, paragraphs, - and 1. lists,
    > quotes, | tables |, **bold**, *italic*, `code` and [links](url)."""
    out, para, lst, lines, i = [], [], None, text.strip().splitlines(), 0

    def flush():
        nonlocal para, lst
        if para:
            out.append(f"<p>{md_inline(' '.join(para))}</p>")
            para = []
        if lst:
            out.append(f"<{lst[0]}>" + "".join(f"<li>{md_inline(x)}</li>" for x in lst[1]) + f"</{lst[0]}>")
            lst = None
    while i < len(lines):
        ln = lines[i].strip()
        i += 1
        if not ln:
            flush()
            continue
        m = re.match(r"(#{2,4})\s+(.*)", ln)
        if m:
            flush()
            n = len(m.group(1))
            out.append(f'<h{n} id="{slugify(m.group(2))}">{md_inline(m.group(2))}</h{n}>')
            continue
        m = re.match(r"(?:[-*]|(\d+)\.)\s+(.*)", ln)
        if m:
            kind = "ol" if m.group(1) else "ul"
            if para:
                out.append(f"<p>{md_inline(' '.join(para))}</p>")
                para = []
            if lst and lst[0] != kind:
                flush()
            lst = lst or (kind, [])
            lst[1].append(m.group(2))
            continue
        if ln.startswith(">"):
            flush()
            q = [ln.lstrip("> ")]
            while i < len(lines) and lines[i].strip().startswith(">"):
                q.append(lines[i].strip().lstrip("> "))
                i += 1
            out.append(f"<blockquote><p>{md_inline(' '.join(q))}</p></blockquote>")
            continue
        if ln.startswith("|"):
            flush()
            rows = [ln]
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows if not re.match(r"^\|[\s:|-]+\|$", r)]
            th = "".join(f'<th scope="col">{md_inline(c)}</th>' for c in cells[0])
            tb = "".join("<tr>" + "".join((f'<th scope="row">{md_inline(c)}</th>' if k == 0 else f"<td>{md_inline(c)}</td>") for k, c in enumerate(r)) + "</tr>" for r in cells[1:])
            out.append(f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>')
            continue
        if lst:
            flush()
        para.append(ln)
    flush()
    return "\n".join(out)


def load_posts():
    posts = []
    for f in sorted(BLOG_DIR.glob("*.md")):
        raw = f.read_text(encoding="utf8").replace("\r\n", "\n")
        m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
        if not m:
            raise SystemExit(f"{f.name}: missing the --- front matter block")
        meta = {}
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip().strip('"')
        for k in ("title", "description", "date", "category"):
            if not meta.get(k):
                raise SystemExit(f"{f.name}: front matter needs '{k}'")
        body = m.group(2)
        words = len(re.findall(r"[A-Za-z0-9']+", body))
        y, mo, da = (int(x) for x in meta["date"].split("-"))
        posts.append(dict(meta, slug=f.stem, body=body, words=words, mins=max(1, round(words / 220)),
                          nice=f"{da} {MONTHS[mo - 1]} {y}", order=int(meta.get("order", 99))))
    posts.sort(key=lambda p: p["order"])
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def post_card(p, tag="h2"):
    c = CAT_COLOR.get(p["category"], "blue")
    return (f'<li class="pcard" style="--c:var(--m-{c})"><a href="/blog/{p["slug"]}/">'
            f'<span class="cat"><i class="cap-ic"></i>{e(p["category"])}</span>'
            f'<{tag}>{e(p["title"])}</{tag}><p>{e(p["description"])}</p>'
            f'<span class="meta">{p["nice"]} · {p["mins"]} min read</span></a></li>')


def blog_index(a, posts):
    d = L["en"]
    cats = []
    for p in posts:
        if p["category"] not in cats:
            cats.append(p["category"])
    chips = "".join(f'<li style="--c:var(--m-{CAT_COLOR.get(c, "blue")})"><i class="cap-ic"></i>{e(c)}</li>' for c in cats)
    ld = json.dumps({"@context": "https://schema.org", "@type": "Blog", "name": "SiteWhiteboard Blog", "url": a.domain + "/blog/",
                     "inLanguage": "en", "description": d["blog_desc"],
                     "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f'{a.domain}/blog/{p["slug"]}/', "datePublished": p["date"]} for p in posts]},
                    ensure_ascii=False)
    body = f"""<main class="blog">
<section class="b-hero"><div class="wrap">
  <span class="badge"><i></i>{e(d['blog'])}</span>
  <h1>Ideas for your <span class="hand">whiteboard</span></h1>
  <p class="lead">{e(d['blog_lead'])}</p>
  <ul class="chips" aria-label="Topics">{chips}</ul>
</div></section>
<div class="wrap"><ul class="posts">{''.join(post_card(p) for p in posts)}</ul></div>
</main>
{ad('en', 'bottom')}<script type="application/ld+json">{ld}</script>
"""
    return head(a, "en", "blog", "Online Whiteboard Blog: Guides for Teaching, Study and Brainstorming | SiteWhiteboard", d["blog_desc"], path="/blog/") + body + foot(a, "en", "blog")


def blog_post(a, p, posts):
    d = L["en"]
    link = f'{a.domain}/blog/{p["slug"]}/'
    same = [x for x in posts if x is not p and x["category"] == p["category"]]
    rest = [x for x in posts if x is not p and x not in same]
    related = (same + rest)[:3]
    c = CAT_COLOR.get(p["category"], "blue")
    ld = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "headline": p["title"], "description": p["description"], "datePublished": p["date"], "dateModified": p.get("updated", p["date"]),
         "inLanguage": "en", "wordCount": p["words"], "articleSection": p["category"], "url": link, "mainEntityOfPage": link,
         "keywords": p.get("keywords", ""),
         "author": {"@type": "Organization", "name": "SiteWhiteboard", "url": a.domain + "/"},
         "publisher": {"@type": "Organization", "name": "SiteWhiteboard", "url": a.domain + "/", "logo": {"@type": "ImageObject", "url": a.domain + "/assets/icon.svg"}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": a.domain + "/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": a.domain + "/blog/"},
            {"@type": "ListItem", "position": 3, "name": p["title"], "item": link}]}]}, ensure_ascii=False)
    extra = f'<meta property="article:published_time" content="{p["date"]}"><meta property="article:section" content="{e(p["category"])}">'
    body = f"""<main class="post" style="--c:var(--m-{c})">
<article>
<header class="p-head"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/blog/">{e(d['blog'])}</a><span aria-hidden="true">/</span><span>{e(p['category'])}</span></nav>
  <h1>{e(p['title'])}</h1>
  <p class="lead">{e(p['description'])}</p>
  <p class="meta"><time datetime="{p['date']}">{p['nice']}</time> · {p['mins']} {e(d['read'])}</p>
</div></header>
<div class="wrap prose">
{md(p['body'])}
<aside class="trynote"><h2>{e(d['try_h'])}</h2><p>{e(d['try_p'])}</p><a class="cta" href="/board/">{e(d['open'])}{ARROW}</a></aside>
</div>
</article>
{ad('en', 'bottom')}<section class="related"><div class="wrap">
  <h2>{e(d['related'])}</h2>
  <ul class="posts">{''.join(post_card(x, 'h3') for x in related)}</ul>
  <a class="cta ghost center" href="/blog/">{e(d['all_posts'])}</a>
</div></section>
</main>
<script type="application/ld+json">{ld}</script>
"""
    return head(a, "en", "blog", p.get("seo_title") or p["title"] + " | SiteWhiteboard", p["description"], path=f'/blog/{p["slug"]}/', og="article", extra=extra) + body + foot(a, "en", "blog")


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
    global SITE_CSS
    SITE_CSS = minify_css((DIST / "assets/site.css").read_text(encoding="utf8"))
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
        pages = {"index": landing(a, lang), "about": about(a, lang), "contact": contact(a, lang),
                 "privacy": doc(a, lang, "privacy", d["privacy_t"], sections(a, lang, d["privacy_s"])),
                 "terms": doc(a, lang, "terms", d["terms_t"], sections(a, lang, d["terms_s"]))}
        for name, text in pages.items():
            (base / (name + ".html")).write_text(text, encoding="utf8")
            urls.append(a.domain + url(lang, name))
    # blog (English): /blog/ and /blog/<slug>/
    posts = load_posts()
    (DIST / "blog").mkdir()
    (DIST / "blog/index.html").write_text(blog_index(a, posts), encoding="utf8")
    for p in posts:
        (DIST / "blog" / p["slug"]).mkdir()
        (DIST / "blog" / p["slug"] / "index.html").write_text(blog_post(a, p, posts), encoding="utf8")
    urls += [a.domain + "/blog/"] + [f'{a.domain}/blog/{p["slug"]}/' for p in posts]

    today = datetime.date.today().isoformat()
    groups = [[board(x) for x in LANGS]] + [[url(x, p) for x in LANGS] for p in ("index", "about", "contact", "privacy", "terms")]
    prio = {"index": "1.0", "board": "0.9", "about": "0.5", "contact": "0.4", "privacy": "0.3", "terms": "0.3"}
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for g in groups:
        kind = "board" if g[0].endswith("/board/") else ("index" if g[0] == "/" else g[0].strip("/").split(".")[0])
        links = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{x}" href="{a.domain}{g[n]}"/>' for n, x in enumerate(LANGS))
        links += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{a.domain}{g[0]}"/>'
        for u in g:
            out.append(f"  <url>\n    <loc>{a.domain}{u}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>{prio[kind]}</priority>{links}\n  </url>")
    newest = max([p.get("updated", p["date"]) for p in posts], default=today)
    out.append(f"  <url>\n    <loc>{a.domain}/blog/</loc>\n    <lastmod>{newest}</lastmod>\n    <priority>0.8</priority>\n  </url>")
    for p in posts:
        out.append(f'  <url>\n    <loc>{a.domain}/blog/{p["slug"]}/</loc>\n    <lastmod>{p.get("updated", p["date"])}</lastmod>\n    <priority>0.7</priority>\n  </url>')
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
