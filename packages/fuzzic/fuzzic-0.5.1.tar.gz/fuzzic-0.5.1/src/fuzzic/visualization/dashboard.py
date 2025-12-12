import base64
import io
import os
import copy
import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def get_img_base64(fig):
    """Convertit une figure Matplotlib en chaîne Base64 pour l'HTML."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig) 
    return img_str

def get_local_image_base64(filename):
    """
    Charge une image locale et la convertit en Base64 en utilisant __file__ pour le chemin.
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, filename)
    except NameError:
        full_path = filename # Fallback
    
    if not os.path.exists(full_path):
        return None
    
    try:
        with open(full_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Erreur image: {e}")
        return None

def get_score_style(score, is_total=False):
    """Retourne une chaîne de style CSS (background-color et color)."""
    if score is None: score = 0
    score = max(0, min(1, score))
    
    hue = score * 120 
    
    if is_total:
        bg_color = f"hsl({hue}, 70%, 45%)"
        text_color = "white"
    else:
        bg_color = f"hsl({hue}, 85%, 92%)"
        text_color = f"hsl({hue}, 90%, 20%)"

    return f"background-color: {bg_color}; color: {text_color};"

def plot_variable_for_html(variable):
    all_sef = variable.all_sef
    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=100) 
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
    
    for i, sef in enumerate(all_sef):
        color = colors[i % len(colors)]
        
        if sef.shape == "gaussian":
            mu = sef.gaussian.mean
            sigma = sef.gaussian.deviation
            x = np.linspace(variable.bounds[0], variable.bounds[1], 500)
            y = np.exp(-(x - mu)**2 / (2 * sigma**2))
            ax.plot(x, y, color=color, label=sef.label, linewidth=2)
            
        else:
            points = sef.points
            x_vals = [p.x for p in points]
            y_vals = [p.y for p in points]
            
            if x_vals[0] > variable.bounds[0]:
                x_vals.insert(0, variable.bounds[0])
                y_vals.insert(0, y_vals[0])
            if x_vals[-1] < variable.bounds[1]:
                x_vals.append(variable.bounds[1])
                y_vals.append(y_vals[-1])
                
            ax.plot(x_vals, y_vals, color=color, label=sef.label, linewidth=2)

    ax.set_ylim(0, 1.1) 
    ax.set_xlim(variable.bounds[0], variable.bounds[1])
    ax.set_title(f"Variable : {variable.label} ({variable.unit})", pad=20)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylabel("Degré d'appartenance")
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
              fancybox=True, shadow=False, ncol=3)

    return get_img_base64(fig)

# =============================================================================
# FONCTION PRINCIPALE
# =============================================================================

def get_dashboard(rulebases):
    """
    Génère un dashboard HTML avec infobulles pour les warnings.
    """
    
    if not isinstance(rulebases, list):
        rulebases = [rulebases]

    logo_base64 = get_local_image_base64("fuzzic.jpg")
    
    logo_html = ""
    if logo_base64:
        logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" class="app-logo" alt="Fuzzic Logo">'
    
    # 1. Début HTML & CSS
    html_start = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard - FUZZy Interpretability Checker</title>
        <style>
            :root { 
                --primary: #2c3e50; 
                --secondary: #3498db; 
                --bg: #f4f7f6; 
                --card-bg: #ffffff; 
                --dark-bg: #dfe6e9;
                --warning-color: #d35400;
            }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--bg); color: #333; margin: 0; padding: 20px; }
            h1, h2, h3 { color: var(--primary); margin-top: 0; }
            
            /* HEADER */
            .brand-header {
                display: flex;
                align-items: center;
                gap: 20px;
                margin-bottom: 25px;
                padding-bottom: 15px;
                border-bottom: 2px solid #e0e0e0;
            }
            .app-logo {
                width: 60px;
                height: 60px;
                border-radius: 12px;
                object-fit: cover;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .app-title {
                font-size: 1.8em;
                font-weight: 800;
                color: var(--primary);
                letter-spacing: -0.5px;
            }

            /* Navigation */
            .nav-container { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; background: var(--card-bg); padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .btn { background-color: var(--secondary); color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; transition: background 0.3s; }
            .btn:hover { background-color: #2980b9; }
            .btn:disabled { background-color: #bdc3c7; cursor: not-allowed; }
            .page-indicator { font-weight: bold; font-size: 18px; }

            /* Contenu */
            .rulebase-container { display: none; animation: fadeIn 0.4s ease-in-out; }
            .rulebase-container.active { display: block; }
            
            .header-section { display: flex; gap: 20px; margin-bottom: 20px; flex-wrap: wrap;}
            .info-box { flex: 1; background: var(--card-bg); padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); border-left: 5px solid var(--secondary); min-width: 300px; }
            .scores-box { flex: 2; background: var(--card-bg); padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); display: flex; gap: 20px; min-width: 400px; }
            
            .total-score-card {
                flex: 0 0 160px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                color: white;
                border-radius: 12px;
                padding: 15px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                text-align: center;
                transition: background 0.5s;
            }
            .total-score-value { font-size: 2.5em; font-weight: bold; line-height: 1; text-shadow: 1px 1px 3px rgba(0,0,0,0.2); }
            .total-score-label { font-size: 0.9em; text-transform: uppercase; margin-top: 5px; opacity: 0.95; font-weight: 600; }
            
            /* Grille petits scores */
            .mini-scores-grid { flex: 1; display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 10px; align-content: start; }
            
            /* ---- STYLE SCORE ITEM + TOOLTIP ---- */
            .mini-score-item { 
                position: relative; /* IMPORTANT pour l'ancrage de la bulle */
                border: 1px solid rgba(0,0,0,0.05); 
                padding: 10px 12px; 
                border-radius: 8px; 
                display: flex; 
                justify-content: space-between; 
                align-items: center; 
                font-size: 0.85em; 
                font-weight: 600;
                transition: transform 0.2s;
            }
            .mini-score-item.has-warning {
                cursor: help; /* Change le curseur pour indiquer qu'il y a une info */
                border-color: rgba(211, 84, 0, 0.3); /* Bordure orange légère */
            }
            .mini-score-item.has-warning:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }

            .mini-score-label { opacity: 0.8; font-weight: normal; display: flex; align-items: center; gap: 5px;}
            .mini-score-val { font-weight: bold; font-size: 1.1em;}
            
            .warning-icon { color: var(--warning-color); font-size: 1.1em; animation: pulse 2s infinite;}

            /* LA BULLE (TOOLTIP) */
            .tooltip-text {
                visibility: hidden;
                width: 280px;
                background-color: #2d3436;
                color: #fff;
                text-align: left;
                border-radius: 6px;
                padding: 12px;
                position: absolute;
                z-index: 100;
                bottom: 120%; /* Affiché au dessus */
                left: 50%;
                transform: translateX(-50%); /* Centré horizontalement */
                opacity: 0;
                transition: opacity 0.3s, bottom 0.3s;
                font-size: 0.9em;
                font-weight: normal;
                line-height: 1.4;
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                pointer-events: none;
                white-space: normal; /* Permet le retour à la ligne */
            }

            /* La petite flèche en bas de la bulle */
            .tooltip-text::after {
                content: "";
                position: absolute;
                top: 100%; /* En bas de la bulle */
                left: 50%;
                margin-left: -5px;
                border-width: 5px;
                border-style: solid;
                border-color: #2d3436 transparent transparent transparent;
            }

            /* Apparition au survol */
            .mini-score-item:hover .tooltip-text {
                visibility: visible;
                opacity: 1;
                bottom: 130%; /* Petit effet de glissement vers le haut */
            }

            @keyframes pulse { 0% { opacity: 0.6; } 50% { opacity: 1; } 100% { opacity: 0.6; } }

            /* Autres styles inchangés... */
            .variables-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(450px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .variable-card { background: var(--card-bg); padding: 10px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); text-align: center; }
            .variable-card img { max-width: 100%; height: auto; }

            .rules-section { background-color: var(--dark-bg); padding: 20px; border-radius: 10px; border: 1px solid #d1d8dd; }
            .rules-table { width: 100%; border-collapse: separate; border-spacing: 0 15px; } 
            .rule-row { transition: transform 0.2s; }
            .rule-row:hover { transform: translateY(-3px); }
            
            .rule-cell-content { position: relative; padding: 20px; }
            .rule-cell { background: #ffffff; vertical-align: middle; border-top: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); padding: 0; }
            .rule-id-cell { text-align: center; font-size: 0.8em; font-weight: 600; color: #555; background: #eaf1f8; width: 70px; }
            .rule-cell:first-child { border-left: 1px solid #e0e0e0; border-top-left-radius: 10px; border-bottom-left-radius: 10px; border-left: 6px solid var(--secondary); }
            .rule-cell:last-child { border-right: 1px solid #e0e0e0; border-top-right-radius: 10px; border-bottom-right-radius: 10px; }
            
            .rules-header th { text-transform: uppercase; font-size: 0.85em; color: #636e72; padding-bottom: 10px; padding-left: 10px;}
            .operator { font-weight: bold; color: #bdc3c7; display: block; margin: 8px 0; font-size: 0.8em; text-align: center; letter-spacing: 1px;}
            .condition { background: #f1f2f6; padding: 6px 12px; border-radius: 20px; display: block; border: 1px solid #dcdde1; }
            .var-name { font-weight: 700; color: #2c3e50; font-size: 0.95em;}
            .sef-name { color: var(--secondary); font-weight: 600; }
            .arrow-col { text-align: center; font-size: 2em; color: var(--secondary); font-weight: bold; width: 60px; }

            @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        </style>
    </head>
    <body>
    """

    header_html = f"""
    <div class="brand-header">
        {logo_html}
        <div class="app-title">Dashboard - FUZZy Interpretability Checker</div>
    </div>
    """

    nav_html = """
    <div class="nav-container">
        <button class="btn" id="prevBtn" onclick="changeSlide(-1)">❮ Previous</button>
        <span class="page-indicator" id="pageIndicator">Chargement...</span>
        <button class="btn" id="nextBtn" onclick="changeSlide(1)">Next ❯</button>
    </div>

    <div id="main-content">
    """
    
    html_content = html_start + header_html + nav_html

    for index, rb in enumerate(rulebases):
        active_class = "active" if index == 0 else ""
        filename = getattr(rb, 'filename', 'inconnu.xml')
        label = rb.label if rb.label else f"Rule base #{index+1}"
        
        s_data = {}
        scores_attr = getattr(rb, 'interpretability', None)
        if scores_attr:
            s_data = copy.deepcopy(scores_attr)

        scores_html = ""
        total_html = ""
        
        if s_data:
            total_obj = s_data.pop('total', None)
            total_val_str = "N/A"
            total_style = "background-color: #95a5a6; color: white;" 
            
            if total_obj and 'score' in total_obj:
                raw_score = total_obj['score']
                total_val_str = f"{int(round(raw_score * 100))}%"
                total_style = get_score_style(raw_score, is_total=True)
            
            total_html = f"""
            <div class="total-score-card" style="{total_style}">
                <div class="total-score-value">{total_val_str}</div>
                <div class="total-score-label">Interpretability Global Score</div>
            </div>
            """
            
            grid_items = ""
            for k, v in sorted(s_data.items()):
                raw_score = 0
                score_str = "?"
                warning_text = ""
                
                if isinstance(v, dict):
                    if 'score' in v:
                        raw_score = v['score']
                        score_str = f"{int(round(raw_score * 100))}%"
                    # Extraction du warning
                    if 'warning' in v and v['warning']:
                        warning_text = v['warning']
                
                item_style = get_score_style(raw_score, is_total=False)
                
                # Logique conditionnelle pour le warning
                if warning_text:
                    # Cas AVEC warning : Classe spéciale, icône et bulle tooltip
                    warning_html = f'<span class="warning-icon" title="Warning">⚠️</span>'
                    tooltip_html = f'<span class="tooltip-text">{warning_text}</span>'
                    
                    grid_items += f"""
                    <div class="mini-score-item has-warning" style="{item_style}">
                        <span class="mini-score-label">{k} {warning_html}</span>
                        <span class="mini-score-val">{score_str}</span>
                        {tooltip_html}
                    </div>
                    """
                else:
                    # Cas SANS warning : Affichage standard
                    grid_items += f"""
                    <div class="mini-score-item" style="{item_style}">
                        <span class="mini-score-label">{k}</span>
                        <span class="mini-score-val">{score_str}</span>
                    </div>
                    """
                    
            scores_html = f"{total_html}<div class=\"mini-scores-grid\">{grid_items}</div>"
        else:
            scores_html = "<div style='padding:10px; color: gray; font-style: italic;'>Attribut .interpretability empty or not found.</div>"

        html_content += f"""
        <div class="rulebase-container {active_class}" data-index="{index}">
            <div class="header-section">
                <div class="info-box">
                    <h2>{label}</h2>
                    <p><strong>File:</strong> {filename}</p>
                    <p><strong>Configuration:</strong> {len(rb.var)} variables, {len(rb.rules)} rules.</p>
                </div>
                <div class="scores-box">
                    {scores_html}
                </div>
            </div>
            
            <h3>Variables</h3>
            <div class="variables-grid">
        """

        for var_key, variable in rb.var.items():
            img_base64 = plot_variable_for_html(variable)
            html_content += f"""
                <div class="variable-card">
                    <img src="data:image/png;base64,{img_base64}" alt="{variable.label}">
                </div>
            """
        
        html_content += """
            </div>
            <h3>Rule base</h3>
            <div class="rules-section">
            <table class="rules-table">
                <thead>
                    <tr class="rules-header">
                        <th style="width: 70px;">ID</th>
                        <th style="width: 40%">Premisses (IF)</th>
                        <th style="width: 5%"></th>
                        <th style="width: 40%">Conclusions (THEN)</th>
                    </tr>
                </thead>
                <tbody>
        """

        rules_list = list(rb.rules.values())
        
        def get_conclusion_sort_key(rule):
            conclusions = sorted(list(rule.conclusion), key=lambda t: t.var.label)
            return "_".join([f"{c.var.label}_{c.sef.label}" for c in conclusions])

        sorted_rules = sorted(rules_list, key=get_conclusion_sort_key)

        for rule in sorted_rules:
            rule_id = getattr(rule, 'ident', 'ID Inconnu')
            
            premisses_html = ""
            sorted_premisses = sorted(list(rule.premisse), key=lambda t: t.var.label)
            for idx, term in enumerate(sorted_premisses):
                premisses_html += f'<span class="condition"><span class="var-name">{term.var.label}</span> is <span class="sef-name">{term.sef.label}</span></span>'
                if idx < len(sorted_premisses) - 1:
                    premisses_html += '<span class="operator">AND</span>'
            
            conclusions_html = ""
            sorted_conclusions = sorted(list(rule.conclusion), key=lambda t: t.var.label)
            for idx, term in enumerate(sorted_conclusions):
                conclusions_html += f'<span class="condition"><span class="var-name">{term.var.label}</span> is <span class="sef-name">{term.sef.label}</span></span>'
                if idx < len(sorted_conclusions) - 1:
                    conclusions_html += '<span class="operator">AND</span>'

            html_content += f"""
                <tr class="rule-row">
                    <td class="rule-cell rule-id-cell">{rule_id}</td>
                    <td class="rule-cell">
                        <div class="rule-cell-content">
                            {premisses_html}
                        </div>
                    </td>
                    <td class="rule-cell arrow-col">&rarr;</td>
                    <td class="rule-cell">
                        <div class="rule-cell-content">
                            {conclusions_html}
                        </div>
                    </td>
                </tr>
            """

        html_content += """
                </tbody>
            </table>
            </div>
        </div>
        """

    html_content += f"""
    </div>

    <script>
        let currentIndex = 0;
        const totalSlides = {len(rulebases)};
        const slides = document.getElementsByClassName("rulebase-container");
        const prevBtn = document.getElementById("prevBtn");
        const nextBtn = document.getElementById("nextBtn");
        const pageIndicator = document.getElementById("pageIndicator");

        function showSlide(n) {{
            for (let i = 0; i < slides.length; i++) {{
                slides[i].classList.remove("active");
            }}
            
            if (n >= totalSlides) currentIndex = 0;
            if (n < 0) currentIndex = totalSlides - 1;

            slides[currentIndex].classList.add("active");
            pageIndicator.textContent = "Rule base " + (currentIndex + 1) + " / " + totalSlides;
            prevBtn.disabled = (currentIndex === 0);
            nextBtn.disabled = (currentIndex === totalSlides - 1);
        }}

        function changeSlide(n) {{
            currentIndex += n;
            showSlide(currentIndex);
        }}

        showSlide(0);
    </script>
    </body>
    </html>
    """

    return html_content