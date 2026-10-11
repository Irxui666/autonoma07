from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
root=Path('tarea07-frontend'); docs=root/'docs'; docs.mkdir(exist_ok=True)
styles=getSampleStyleSheet(); styles['BodyText'].fontSize=9; styles['BodyText'].leading=12; styles['BodyText'].spaceAfter=7
styles['Code'].fontSize=6.6;styles['Code'].leading=8
story=[]; md=[]
def h(t): story.append(Paragraph(escape(t),styles['Heading2']));md.append('\n## '+t+'\n')
def p(t): story.append(Paragraph(escape(t),styles['BodyText']));md.append(t+'\n')
def code(t): story.append(Preformatted(t,styles['Code']));md.append('```\n'+t+'\n```\n')
def table(rows,widths):
    t=Table([[Paragraph(escape(str(c)),styles['BodyText']) for c in row] for row in rows],colWidths=widths,repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5edf4')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#bccbd8')),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5)]));story.append(t)
    md.extend([' | '.join(map(str,r))+'\n' for r in rows])
def ref(file,needle):
    lines=(root/file).read_text(encoding='utf-8').splitlines(); n=next(i for i,l in enumerate(lines,1) if needle in l);return f'{file}:{n}'
def page():story.append(PageBreak());md.append('\n---\n')
h('PharmaSoft | Informe técnico de arquitectura')
p('Lenguaje de Programación II · Actividad autónoma de la sesión 7 · 11 de octubre de 2026. Autor: pendiente de completar con el nombre del estudiante.')
p('Alcance: revisión y adaptación del módulo Clientes existente en tarea07-frontend, con compatibilidad del backend local. Este informe describe el código entregado; las evidencias de navegador y la entrega Git se identifican como pendientes cuando no se han ejecutado.')
h('B1. Estructura del proyecto')
paths=sorted((root/'src/app').rglob('*')); tree=['src/app/']
for f in paths:
    if f.is_file():
        rel=f.relative_to(root/'src/app'); tree.append('  '*(len(rel.parts)-1)+f.name)
for folder in ['core','shared','layout','features']:
    pass
code('src/app/\n  app.ts, app.html, app.css, app.config.ts, app.routes.ts\n  core/\n    config/menu.ts\n    models/{error-response,pagina-response}.ts\n    utils/{http-error,numeros,texto}.ts\n  shared/pages/no-encontrado/ [ts, html, css]\n  layout/{header,sidebar,main-layout}/ [ts, html, css]\n  features/\n    inicio/ [ts, html, css]\n    categorias/\n      categorias.routes.ts\n      models/categoria.model.ts\n      services/categoria-service.ts\n      pages/{categoria-list,categoria-form}/ [ts, html, css]\n    clientes/\n      clientes.routes.ts\n      models/cliente.model.ts\n      services/cliente-service.ts\n      pages/{cliente-list,cliente-form}/ [ts, html]\n    productos/\n      productos.routes.ts\n      models/producto.model.ts\n      services/producto-service.ts\n      pages/{producto-list,producto-form}/ [ts, html]')
p('Árbol agrupado de archivos de producción. El árbol completo, incluidos los archivos .spec.ts, está en docs/arbol-src-app.txt. Productos existe en disco, pero no está registrado en las rutas principales ni en MENU.')
p('core reúne configuración, contratos y utilidades transversales; shared contiene la página reutilizable de error 404; layout mantiene la estructura visual; features agrupa cada dominio con modelos, servicio, páginas y rutas. La paginación se comparte mediante PaginaResponse<T>, mientras que las reglas de Clientes permanecen en su feature.')
code("// " +ref('src/app/features/clientes/services/cliente-service.ts','private readonly url')+'\nprivate readonly url = `${environment.apiUrl}/clientes`;\n// '+ref('src/app/features/clientes/pages/cliente-form/cliente-form.ts','const dto')+'\nconst dto: ClienteRequest = { ...v, telefono: v.telefono || null, direccion: v.direccion || null };')
page();h('B2. Mapa completo de rutas activas')
table([['URL','Componente / padre','Carga','Título'],['/','Redirección a /inicio / MainLayout','Redirección','Hereda destino'],['/inicio','Inicio / MainLayout','loadComponent','PharmaSoft'],['/categorias','CategoriaList / MainLayout','loadChildren → component','Categorías'],['/categorias/nuevo','CategoriaForm / MainLayout','loadChildren → component','Nueva categoría'],['/categorias/:id/editar','CategoriaForm / MainLayout','loadChildren → component','Editar categoría'],['/clientes','ClienteList / MainLayout','loadChildren → component','Clientes'],['/clientes/nuevo','ClienteForm / MainLayout','loadChildren → component','Nuevo cliente'],['/clientes/:id/editar','ClienteForm / MainLayout','loadChildren → component','Editar cliente'],['/**','NoEncontrado / sin padre','loadComponent','Página no encontrada']],[123,160,117,87])
p('Fuentes: '+ref('src/app/app.routes.ts','export const routes')+'; '+ref('src/app/features/clientes/clientes.routes.ts','export const CLIENTES')+'; '+ref('src/app/features/categorias/categorias.routes.ts','export const CATEGORIAS')+'. MainLayout se importa directamente; los componentes de cada feature se importan desde su archivo de rutas diferido.')
h('B3. Responsabilidades y límites')
table([['Pieza','Qué hace','Qué no hace'],['ClienteService / servicio','Cinco operaciones HTTP tipadas, parámetros de página.','No presenta mensajes ni navega.'],['ClienteList / componente','Signals, filtro computed, orden, página y baja.','No construye HTTP ni valida unicidad.'],['ClienteForm / componente','Validación, carga por ID, DTO, guardar y navegar.','No decide unicidad ni persiste directamente.'],['CategoriaService / servicio','Encapsula HTTP de Categorías.','No controla la vista.'],['CategoriaList / componente','Carga, búsqueda local y eliminación de categorías.','No conoce URL ni consulta la base de datos.'],['CategoriaForm / componente','Formulario reactivo, edición y errores.','No implementa reglas de integridad del servidor.'],['MainLayout / componente','Header, Sidebar, outlet y menú colapsado.','No administra entidades.'],['Header / componente','Marca, enlaces y evento toggleMenu.','No consulta clientes.'],['Sidebar / componente','Recorre MENU y marca ruta activa.','No realiza CRUD ni autentica usuarios.']],[112,190,185])
page();h('B4. Flujo de registrar cliente')
p('El diagrama sigue las llamadas reales del formulario y del listado; el signal de clientes se actualiza después del GET posterior a la navegación, no con el POST directamente.')

from reportlab.graphics.shapes import Drawing,Rect,String,Line,Polygon
d=Drawing(480,310)
def box(x,y,w,label):
 d.add(Rect(x,y,w,36,rx=5,fillColor=colors.HexColor('#e8f0f7'),strokeColor=colors.HexColor('#416784')))
 d.add(String(x+8,y+14,label,fontName='Helvetica',fontSize=9))
def arrow(x,y,x2,y2):
 d.add(Line(x,y,x2,y2,strokeColor=colors.HexColor('#416784')));d.add(Polygon([x2,y2,x2-4,y2+7,x2+4,y2+7],fillColor=colors.HexColor('#416784')))
box(105,270,270,'Clic Guardar → ClienteForm.guardar()');arrow(240,270,240,246)
box(105,210,270,'Validar → DTO (opcionales vacíos = null)');arrow(240,210,240,186)
box(105,150,270,'ClienteService.crear(dto) → POST /clientes');arrow(240,150,240,126)
box(105,90,270,'PharmaBackend: validar y persistir')
d.add(Line(165,90,100,64));d.add(Line(310,90,380,64))
box(0,25,232,'201 → navegar /clientes → GET paginado')
box(248,25,232,'409 → error.set(mensajeError(e))')
d.add(String(8,7,'clientes.set(contenido) → computed → fila',fontSize=9))
d.add(String(255,7,'guardando=false; formulario conserva valores',fontSize=9))
story.append(d)
p('Validación local fallida: markAllAsTouched() y retorno antes de invocar al servicio. Un 409 muestra el mensaje del backend, mantiene los datos y permite corregirlos. Un 400 puede mostrar además erroresServidor por campo.')
code('// '+ref('src/app/features/clientes/pages/cliente-form/cliente-form.ts','request.subscribe')+'\nrequest.subscribe({\n  next: () => this.router.navigate([\'/clientes\'], { queryParams: { guardado: 1 } }),\n  error: e => { this.guardando.set(false); this.error.set(mensajeError(e)); /* ... */ }\n});')
p('Fuentes adicionales: '+ref('src/app/features/clientes/pages/cliente-list/cliente-list.ts','this.service.listar')+' (contenido y metadatos), '+ref('src/app/features/clientes/pages/cliente-list/cliente-list.ts','readonly filtrados')+' (computed) y '+ref('src/app/features/clientes/services/cliente-service.ts','crear(dto')+' (POST).')
h('Compatibilidad del backend entregado')
p('La copia local anterior devolvía Iterable y eliminaba físicamente. Se adaptaron ClienteController.java, ClienteService.java y ClienteServiceImpl.java: GET paginado, orden limitado a id/dni/nombres/apellidos/email, parámetros inválidos con 409, baja estado=false y 409 al repetirla. La consulta conserva clientes inactivos y agrega id como desempate del orden. Categorías no se modificó.')
page();h('B5. Preguntas de revisión')
qs=[('1. Archivos modificados y arquitectura','En esta sesión se modificaron tres archivos existentes del frontend: cliente-service.ts, cliente-list.ts y cliente-list.html. Clientes, sus modelos, sus rutas y MENU ya existían. Para agregar el feature desde la base de Categorías, los dos puntos transversales son app.routes.ts y core/config/menu.ts; no se afirma que se hayan modificado ahora. Además se adaptaron tres archivos del backend. La incorporación está localizada en el dominio y no exige cambiar Header o Sidebar. '+ref('src/app/app.routes.ts',"path: 'clientes'")+'; '+ref('src/app/core/config/menu.ts',"etiqueta: 'Clientes'")+'.'),('2. Por qué el listado no usa HttpClient','El listado coordina presentación y estados y depende de ClienteService. La URL base está en environment.apiUrl y el recurso en el servicio; cambiar el servidor exige ajustar el environment correspondiente, sin editar el listado. '+ref('src/app/features/clientes/services/cliente-service.ts','private readonly url')+'; '+ref('src/app/features/clientes/pages/cliente-list/cliente-list.ts','inject(ClienteService)')+'.'),('3. Ventaja concreta de loadChildren','El archivo de rutas y sus imports se descargan cuando se necesita Clientes. app.routes.ts no importa sus páginas directamente; el límite del feature facilita crecimiento y división del bundle. ng build completado: chunk-BMcrz_Lb.js | clientes-routes | 10.43 kB | 3.38 kB estimados de transferencia. Esta salida verifica un chunk diferido del feature; Categorías conserva su chunk independiente. Registro: docs/validacion-build.txt. '+ref('src/app/app.routes.ts',"path: 'clientes'")+'.'),('4. Persistencia del layout','Categorías y Clientes son rutas hijas del mismo MainLayout. El RouterOutlet interno cambia de página y conserva la instancia padre con Header y Sidebar. Puede haber detección de cambios, pero no una recreación del layout por cada navegación entre esas hijas. '+ref('src/app/layout/main-layout/main-layout.html','router-outlet')+'; '+ref('src/app/app.routes.ts','children:')+'.'),('5. Ocultar Clientes por permisos','El punto de definición es core/config/menu.ts. Allí se añadiría el permiso requerido y el Sidebar filtraría los elementos según el usuario; el Sidebar actual solo recorre MENU y todavía no implementa ese filtro. Centralizar los datos evita duplicar decisiones por página, pero ocultar el enlace no protege la URL: también hacen falta guards y autorización en backend. '+ref('src/app/core/config/menu.ts','export const MENU')+'; '+ref('src/app/layout/sidebar/sidebar.html','@for')+'.'),('6. Duplicación y propuesta','Los formularios repiten estados de carga, guardado, errores y navegación; los listados repiten búsqueda y presentación de errores. Se propone un componente de alerta y controles de paginación en shared, conservando validadores y DTO por dominio. No conviene un CRUD genérico que confunda baja lógica de Clientes y eliminación de Categorías. '+ref('src/app/features/clientes/pages/cliente-form/cliente-form.ts','readonly guardando')+'; '+ref('src/app/features/categorias/pages/categoria-form/categoria-form.ts','readonly guardando')+'.'),('7. Búsqueda limitada a la página','filtrados depende de clientes(), que contiene únicamente respuesta.contenido. El computed no realiza peticiones. Para buscar globalmente, el backend debe aceptar un parámetro de búsqueda y filtrar en la consulta antes de paginar y contar; ClienteService lo enviaría mediante HttpParams. El componente reiniciaría la página y aplicaría debounce y cancelación de solicitudes. '+ref('src/app/features/clientes/pages/cliente-list/cliente-list.ts','readonly filtrados')+'; '+ref('src/app/features/clientes/services/cliente-service.ts','const params')+'.')]
for title,body in qs:h(title);p(body)
page();h('A7. Verificación y evidencias de entrega')
p('Estado: no hay PharmaBackend escuchando en localhost:8080 al revisar el entorno. Los siguientes son casos de aceptación pendientes de ejecución integrada y de captura con la pestaña Red visible. Esta tabla no reemplaza las once capturas exigidas. La compilación y pruebas disponibles se registran por separado en docs/.')
rows=[['N.º','Acción / evidencia que debe guardarse'],['1','Abrir Clientes desde sidebar: activo y GET 200 con pagina=0.'],['2','Tamaño 5 y Siguiente: tamanio=5, pagina=1; Página 2.'],['3','Apellidos dos veces: comprobar asc y desc y cambio de orden.'],['4','DNI de 7 dígitos: validación visible, sin POST.'],['5','Alta válida sin opcionales: POST 201, null y teléfono como guion.'],['6','DNI o correo duplicado: POST 409 y mensaje del backend.'],['7','Editar teléfono: GET precarga y PUT 200 con nueve dígitos.'],['8','Buscar DNI y apellido: filtro local sin nueva petición.'],['9','Baja activa: DELETE 204, GET posterior y estado Inactivo.'],['10','Repetir baja: DELETE 409 y mensaje del backend.'],['11','Regresar a Categorías: comprobar listado y operaciones.']]
table(rows,[30,457])
h('C. Versionamiento y entrega: pendientes verificables')
p('Las carpetas recibidas no contienen un repositorio Git ni remoto. No se puede acreditar una rama creada desde develop, commits históricos ni un pull request. No se generaron fechas falsas. El estudiante debe vincular este trabajo a su repositorio real, crear feature/clientes-<apellido> desde develop y registrar avances reales. El requisito de tres días distintos no puede satisfacerse retroactivamente en esta sesión.')
p('Enlace del pull request hacia develop: pendiente de crear en el repositorio real. Nombre de entrega en aula: Apellido_LP2_S7_Autonoma.pdf, reemplazando Apellido por el del estudiante. Antes de entregar, completar autor, enlace y capturas. El chunk ya se verificó con ng build. El informe se guarda en docs/informe-arquitectura.pdf.')
h('Cómo reproducir')
p('Backend: Java 21, Oracle configurado en application-dev.yaml; ejecutar mvnw.cmd spring-boot:run y comprobar Swagger. Frontend: npm ci, npm run build, npm test -- --watch=false y npm start. Mantener localhost:8080 y localhost:4200 según la configuración del proxy. Guía operativa ampliada: docs/ENTREGA.md.')
def footer(c,d):
 c.setStrokeColor(colors.HexColor('#bccbd8'));c.line(42,38,553,38);c.setFont('Helvetica',8);c.drawString(42,25,'PharmaSoft · LP II · Sesión 7');c.drawRightString(553,25,str(d.page))
SimpleDocTemplate(str(docs/'informe-arquitectura.pdf'),pagesize=(595,842),rightMargin=54,leftMargin=54,topMargin=38,bottomMargin=48).build(story,onFirstPage=footer,onLaterPages=footer)
(docs/'informe-arquitectura.md').write_text('\n'.join(md),encoding='utf-8')
(docs/'arbol-src-app.txt').write_text('\n'.join(tree),encoding='utf-8')
