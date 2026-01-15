import os
import redis
from flask import Flask, render_template, request, redirect, session, url_for, flash
import string
import random

app = Flask(__name__)
app.secret_key = "tu6fgjyuo7i65u7rtgwet3y5y6u" 

# --- REDIS SETUP ---
# Heroku provides the Redis URL via the REDIS_URL environment variable
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

# Use connection_pool to specify SSL settings if the URL starts with 'rediss://'
if redis_url.startswith("rediss://"):
    db = redis.from_url(
        redis_url, 
        decode_responses=True, 
        ssl_cert_reqs=None # This line disables SSL verification
    )
else:
    db = redis.from_url(redis_url, decode_responses=True)

# --- 1. CONTENT DATABASE ---
blog_data = {
    # JEE Articles
    "math-shortcuts": {
        "title": "Top 10 Mathematics Shortcuts for JEE 2026",
        "content": """
            <p class="lead">In the high-pressure environment of JEE Mains and Advanced, time management is just as critical as conceptual knowledge. With only a few minutes allocated per question, the traditional "board exam" methods of solving can cost you your rank. Below are the top 10 mathematical shortcuts and strategies that toppers use to solve problems in seconds.</p>
            
            <hr>

            <h3>1. Integration by Parts: The DI (Tabular) Method</h3>
            <p>The standard formula for integration by parts, <code>&int; u dv = uv - &int; v du</code>, is slow and prone to sign errors, especially when repeated application is needed (like for <code>&int; x^3 e^x dx</code>). Instead, use the <strong>DI Method</strong>:</p>
            <ul>
                <li>Create two columns: <strong>D</strong> (Differentiate) and <strong>I</strong> (Integrate).</li>
                <li>Pick your <code>u</code> (algebraic) for column D and <code>dv</code> for column I.</li>
                <li>Differentiate <code>u</code> down until it hits zero. Integrate <code>dv</code> the same number of times.</li>
                <li>Draw diagonal arrows and apply alternating signs (+, -, +, -).</li>
                <li>Sum the products of the diagonals. This method turns a 5-minute problem into a 30-second one.</li>
            </ul>

            <h3>2. Coordinate Geometry: Conditions of Tangency</h3>
            <p>Approximately 40% of Coordinate Geometry questions in JEE involve finding tangents. Never solve the line equation <code>y = mx + c</code> with the curve equation simultaneously (setting Discriminant = 0) unless absolutely necessary. Instead, memorize the standard conditions of tangency:</p>
            <ul>
                <li><strong>Circle (x² + y² = a²):</strong> <code>c = ±a&radic;(1 + m²)</code></li>
                <li><strong>Parabola (y² = 4ax):</strong> <code>c = a/m</code></li>
                <li><strong>Ellipse (x²/a² + y²/b² = 1):</strong> <code>c = ±&radic;(a²m² + b²)</code></li>
                <li><strong>Hyperbola (x²/a² - y²/b² = 1):</strong> <code>c = ±&radic;(a²m² - b²)</code></li>
            </ul>
            <p>Directly substituting these values allows you to write the equation of the tangent immediately.</p>

            <h3>3. Substitution Method for Algebra & Trigonometry</h3>
            <p>If a question asks for the value of a complex expression that is independent of variables (e.g., "The value of sin^6 x + cos^6 x + 3sin^2 x cos^2 x is..."), do not simplify it. <strong>Substitute a valid value</strong>.</p>
            <p>For example, put <code>x = 0°</code> or <code>x = 90°</code>. If the expression involves variables <code>a, b, c</code> in a determinant, try substituting <code>a=1, b=2, c=3</code> to reduce the matrix to numerical form instantly. <em>Caution: Avoid values that make the denominator zero.</em></p>

            <h3>4. L'Hospital's Rule for Limits</h3>
            <p>While standard limit formulas are important, L'Hospital's Rule is the ultimate weapon for <code>0/0</code> or <code>&infin;/&infin;</code> forms. Differentiate the numerator and denominator separately with respect to x. If the indeterminate form persists, differentiate again. This is often faster than factorization or rationalization.</p>

            <h3>5. Definite Integration: King's Property</h3>
            <p>The property <code>&int;<sub>a</sub><sup>b</sup> f(x) dx = &int;<sub>a</sub><sup>b</sup> f(a + b - x) dx</code> is known as the "King's Property" for a reason. It is the most useful tool in definite integration.</p>
            <p>Whenever you see a complicated denominator involving trigonometry or exponentials in a definite integral, apply this property. Adding the original integral (I) and the new integral (I) often results in the denominator canceling out, leaving a constant (1) to integrate.</p>

            <h3>6. Cayley-Hamilton Theorem for Matrices</h3>
            <p>Finding the inverse of a 3x3 matrix using the adjoint method is tedious. The Cayley-Hamilton theorem states that every square matrix satisfies its own characteristic equation <code>|A - &lambda;I| = 0</code>.</p>
            <p>By finding the characteristic equation (e.g., <code>&lambda;³ - 6&lambda;² + 11&lambda; - 6 = 0</code>), you can replace <code>&lambda;</code> with matrix A. Multiply the entire equation by <code>A⁻¹</code> to directly isolate and find the inverse matrix without calculating cofactors.</p>

            <h3>7. Graphical Approach for "Number of Solutions"</h3>
            <p>If a question asks for the "number of real solutions" for an equation like <code>sin(x) = x/10</code>, do not try to solve it algebraically. It is impossible.</p>
            <p>Instead, draw the graph of <code>y = sin(x)</code> and <code>y = x/10</code> on the same Cartesian plane. Simply count the number of points where the two graphs intersect. This visual method is instantaneous and accurate.</p>

            <h3>8. Dimensional Analysis for Physics & Math</h3>
            <p>While this is a Physics trick, it applies to Math applications (like Area/Volume integration or differential equations). If the options have different dimensions (e.g., one option represents Length², another Length³), and you are calculating Volume, you can eliminate options immediately. In integration, check if the dimension of the answer matches the dimension of the area under the curve.</p>

            <h3>9. Vector Triple Product Expansion</h3>
            <p>Questions involving <code>a x (b x c)</code> are common. Memorize the expansion <strong>"BAC - CAB"</strong> rule:</p>
            <p><code>a x (b x c) = (a·c)b - (a·b)c</code></p>
            <p>This converts a complex vector cross product problem into simpler dot products (scalars) multiplied by vectors.</p>

            <h3>10. Binomial Approximation</h3>
            <p>For questions involving approximation or limits where <code>x</code> is very small (x &lt;&lt; 1), use the binomial approximation: <code>(1 + x)<sup>n</sup> &approx; 1 + nx</code>.</p>
            <p>This is extremely useful in limits and error analysis questions, saving you from expanding the entire series.</p>

            <hr>
            <p class="text-muted"><em>Mastering these shortcuts requires practice. Apply them in your mock tests to verify their speed and accuracy before the final exam.</em></p>
        """
    },
    "organic-chemistry": {
        "title": "Mastering Organic Reaction Mechanisms for Competitive Exams",
        "content": """
            <p class="lead">Organic Chemistry is often the "make or break" section in JEE and NEET. The biggest mistake students make is treating it like a history lesson—memorizing reactions without understanding the <em>why</em>. Mastering the flow of electrons (Reaction Mechanisms) is the secret to solving complex problems without rote memorization.</p>

            <hr>

            <h3>1. The Golden Rule: Follow the Electrons</h3>
            <p>Every organic reaction is essentially a story of electron density moving from a <strong>Nucleophile</strong> (electron-rich, "Nucleus-loving") to an <strong>Electrophile</strong> (electron-deficient, "Electron-loving"). Before solving any reaction, draw the structure and identify:</p>
            <ul>
                <li>Where are the lone pairs or pi-bonds? (Source)</li>
                <li>Where is the positive charge or partial positive charge? (Sink)</li>
            </ul>
            <p>Arrows always flow from Source to Sink. Never draw an arrow starting from a proton (H+).</p>

            <h3>2. GOC: The Foundation of Stability</h3>
            <p>Reaction intermediates (carbocations, carbanions, free radicals) drive the reaction path. Their stability is governed by General Organic Chemistry (GOC) effects:</p>
            <ul>
                <li><strong>Inductive Effect (I-Effect):</strong> Permanent displacement of sigma electrons. +I groups (alkyl) stabilize carbocations; -I groups (halogens, NO2) destabilize them.</li>
                <li><strong>Resonance (Mesomeric Effect):</strong> Delocalization of pi-electrons. This is stronger than the inductive effect. A carbocation adjacent to a double bond (allylic) or benzene ring (benzylic) is exceptionally stable.</li>
                <li><strong>Hyperconjugation:</strong> The "Baker-Nathan" effect. The more alpha-hydrogens an alkene or carbocation has, the more stable it is. (e.g., 3° > 2° > 1°).</li>
            </ul>

            <h3>3. Nucleophilic Substitution: SN1 vs SN2</h3>
            <p>This is the most tested topic. You must distinguish between them instantly:</p>
            <table class="table table-bordered table-striped mt-3">
                <thead class="table-dark">
                    <tr>
                        <th>Feature</th>
                        <th>SN1 Reaction</th>
                        <th>SN2 Reaction</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Kinetics</strong></td>
                        <td>Unimolecular (Rate &prop; [Substrate])</td>
                        <td>Bimolecular (Rate &prop; [Substrate][Nu])</td>
                    </tr>
                    <tr>
                        <td><strong>Mechanism</strong></td>
                        <td>Two Steps (Carbocation Intermediate)</td>
                        <td>Single Step (Transition State)</td>
                    </tr>
                    <tr>
                        <td><strong>Stereochemistry</strong></td>
                        <td>Racemization (Retent + Inversion)</td>
                        <td>Walden Inversion (Umbrella flip)</td>
                    </tr>
                    <tr>
                        <td><strong>Reactivity</strong></td>
                        <td>3° > 2° > 1° > Methyl</td>
                        <td>Methyl > 1° > 2° > 3° (Steric Hindrance)</td>
                    </tr>
                    <tr>
                        <td><strong>Solvent</strong></td>
                        <td>Polar Protic (Water, Alcohol)</td>
                        <td>Polar Aprotic (DMSO, DMF, Acetone)</td>
                    </tr>
                </tbody>
            </table>

            <h3>4. Elimination Reactions: E1 vs E2</h3>
            <p>Elimination competes with substitution. The key factor is <strong>Heat</strong>.</p>
            <ul>
                <li><strong>E1 Mechanism:</strong> Similar to SN1. Forms a carbocation. Favored by weak bases and heat. Always yields the more stable alkene (Saytzeff Product) as the major product.</li>
                <li><strong>E2 Mechanism:</strong> Single step. Requires a strong, bulky base (like Alc. KOH or t-BuOK) and heat. The leaving group and the beta-hydrogen must be <em>anti-periplanar</em> (180° apart).</li>
            </ul>
            <p><strong>Tip:</strong> If the question mentions "Alcoholic KOH" and "Heat," it is almost guaranteed to be an Elimination reaction forming an alkene.</p>

            <h3>5. Important Named Reactions & Tricks</h3>
            <ul>
                <li><strong>Aldol Condensation:</strong> Aldehydes/Ketones with at least one &alpha;-hydrogen react with Dilute NaOH. Trick: Remove water (H2O) from two molecules to join them.</li>
                <li><strong>Cannizzaro Reaction:</strong> Aldehydes <em>without</em> &alpha;-hydrogens (like HCHO, Ph-CHO) react with Conc. NaOH. One molecule oxidizes (Acid salt), the other reduces (Alcohol).</li>
                <li><strong>Reimer-Tiemann:</strong> Phenol + CHCl3 + KOH &rarr; Salicylaldehyde. Remember the intermediate is the electrophile <em>:CCl2 (Dichlorocarbene)</em>.</li>
            </ul>

            <h3>6. Reagents You Must Know</h3>
            <p>Don't just memorize the name; memorize the function:</p>
            <ul>
                <li><strong>LiAlH4:</strong> Strongest reducing agent. Reduces Acids, Esters, Ketones, and Cyanides to Alcohols/Amines.</li>
                <li><strong>NaBH4:</strong> Mild reducing agent. Only reduces Aldehydes, Ketones, and Acid Chlorides. Does NOT touch Esters or Acids.</li>
                <li><strong>PCC / Collins Reagent:</strong> Mild oxidizing agents. Converts 1° Alcohol to Aldehyde (stops oxidation there).</li>
                <li><strong>KMnO4 / K2Cr2O7:</strong> Strong oxidizing agents. Converts 1° Alcohol straight to Carboxylic Acid.</li>
            </ul>

            <hr>
            <p class="text-muted"><em>Organic chemistry is a chain. If you master GOC and Reaction Mechanisms, the chapters on Hydrocarbons, Haloalkanes, and Carbonyl compounds become simply applications of these core principles.</em></p>
        """
    },
    
    # NEET Articles
    "neet-biology": {
        "title": "NEET UG 2026: The Ultimate Blueprint to Score 340+ in Biology",
        "content": """
            <p class="lead">Biology is the backbone of the NEET exam, constituting 50% of the total weightage (360 out of 720 marks). While Physics and Chemistry determine your rank, Biology determines your selection. Scoring 340+ is not just a target; it is a necessity for securing a seat in a government medical college. Here is the detailed roadmap to mastering NEET Biology.</p>
            
            <hr>

            <h3>1. The Holy Grail: Decoding NCERT</h3>
            <p>It is a well-known fact that 90-95% of NEET Biology questions are directly framed from NCERT lines. However, "reading" NCERT is not enough; you must "decode" it.</p>
            <ul>
                <li><strong>Hidden Details:</strong> Questions often come from the captions of diagrams, the summaries at the end of chapters, and the introductory paragraphs of units. Do not skip these.</li>
                <li><strong>Data & Examples:</strong> In chapters like <em>Morphology of Flowering Plants</em> and <em>Animal Kingdom</em>, rote memorization of examples is non-negotiable. Make mnemonic charts for these.</li>
                <li><strong>Scientists & Dates:</strong> Create a separate list of all scientists mentioned (e.g., Darwin, Mendel, Cohen & Boyer) and their specific contributions.</li>
            </ul>

            <h3>2. High-Yield Unit Breakdown</h3>
            <p>Not all chapters are created equal. Prioritize your revision based on weightage trends from the last 10 years:</p>
            
            <h4>A. Genetics & Evolution (12-15 Questions)</h4>
            <p>This is the most conceptual unit. Focus on <em>Molecular Basis of Inheritance</em> (DNA replication, Transcription, Translation, Lac Operon). In <em>Principles of Inheritance</em>, master Pedigree Analysis and Genetic Disorders (Color blindness, Haemophilia, Sickle-cell anemia).</p>
            
            <h4>B. Human Physiology (12-14 Questions)</h4>
            <p>This unit tests your understanding of mechanisms. Pay special attention to:</p>
            <ul>
                <li><strong>Chemical Coordination:</strong> Mechanism of hormone action.</li>
                <li><strong>Neural Control:</strong> Nerve impulse conduction and the structure of the Eye/Ear.</li>
                <li><strong>Breathing & Exchange:</strong> Transport of gases (Oxygen dissociation curve).</li>
            </ul>

            <h4>C. Biotechnology (8-10 Questions)</h4>
            <p>This is a small unit with huge weightage. Questions here are often application-based. Thoroughly understand the tools (Restriction Enzymes, Vectors like pBR322) and processes (PCR, Gel Electrophoresis, RNA Interference).</p>

            <h4>D. Ecology (10-12 Questions)</h4>
            <p>Often ignored by students as "easy," this unit is a goldmine for marks. Focus on:</p>
            <ul>
                <li><strong>Biodiversity Conservation:</strong> In-situ vs Ex-situ conservation examples.</li>
                <li><strong>Environmental Issues:</strong> Pollution data, Acts, and Protocols (Montreal, Kyoto).</li>
                <li><strong>Population Interactions:</strong> Mutualism, Commensalism, etc., with specific examples.</li>
            </ul>

            <h3>3. Diagram-Based Strategy</h3>
            <p>Recent NEET papers have seen a surge in diagram-based questions. You don't need to draw them, but you must be able to label them blindly.</p>
            <p><strong>Critical Diagrams:</strong> Structure of the Heart, Nephron, Sarcomere, pBR322 Vector, and the entire reproductive system. Often, questions ask to identify a part labeled 'A', 'B', or 'C' and state its function.</p>

            <h3>4. The "Fill-in-the-Blanks" Technique</h3>
            <p>To truly test if you know NCERT, try to read a paragraph and then recall the keywords without looking. Many toppers use "Fill-in-the-blank" worksheets derived from NCERT lines to ensure they aren't just passively reading but actively recalling information.</p>

            <h3>5. Practicing for Speed and Accuracy</h3>
            <p>Your target should be to finish the entire Biology section (90 questions) in <strong>45 to 50 minutes</strong>. This leaves you ample time for the calculation-heavy Physics and Chemistry sections.</p>
            <ul>
                <li><strong>Statement Questions:</strong> Practice "Assertion-Reason" and "Choose the Correct Statement" type questions, as these are time-consuming and tricky.</li>
                <li><strong>Match the Column:</strong> These are the easiest to solve using the elimination method. Matching just one or two pairs often gives you the correct answer.</li>
            </ul>

            <h3>6. Common Pitfalls to Avoid</h3>
            <ul>
                <li><strong>Over-reading:</strong> Do not use reference books that go deep into MBBS-level details (like Campbell or Trueman) unless you have finished NCERT 10 times. NEET strictly sticks to the 11th and 12th syllabus.</li>
                <li><strong>Ignoring Plant Physiology:</strong> Many students find cycles (C3, C4, Krebs, Glycolysis) difficult. Make flowcharts for these cycles and paste them on your wall.</li>
            </ul>

            <hr>
            <p class="text-muted"><em>Biology is a race against memory. Consistent revision is the only key. If you are scoring 300, push for 320. If you are at 320, push for 340. That extra margin is what gets you into AIIMS or MAMC.</em></p>
        """
    },
    "neet-physics": {
        "title": "NEET Physics 2026: From Fear Factor to Rank Booster",
        "content": """
            <p class="lead">For the majority of medical aspirants, Physics is the Achilles' heel. It is the subject that creates the gap between a government college seat and a drop year. However, the truth is that NEET Physics is not about becoming a mathematician; it is about understanding concepts and applying them quickly. Here is your comprehensive strategy to score 160+ in NEET Physics.</p>
            
            <hr>

            <h3>1. The 70-30 Rule of Syllabus Weightage</h3>
            <p>Analysis of the last 15 years of NEET papers reveals a clear pattern. Approximately 70% of the questions come from just 30% of the syllabus. Prioritizing these high-yield topics is the smartest way to prepare.</p>
            
            <h4>A. Modern Physics (12-16 Marks)</h4>
            <p>This is the "low hanging fruit" of NEET Physics. Chapters like <em>Atoms</em>, <em>Nuclei</em>, <em>Dual Nature of Radiation</em>, and <em>Semiconductors</em> are almost entirely theoretical or formula-based. The questions are direct, and calculation is minimal. You simply cannot afford to lose marks here.</p>

            <h4>B. Electrodynamics (40-45 Marks)</h4>
            <p>This massive unit includes <em>Electrostatics</em>, <em>Current Electricity</em>, and <em>Magnetism</em>. While it is lengthy, the questions from <em>Current Electricity</em> (Kirchhoff's Laws, Instruments) are standard and repetitive. Master the circuit diagrams and standard instrument errors (Potentiometer, Meter Bridge).</p>

            <h4>C. Mechanics (45-50 Marks)</h4>
            <p>Mechanics is the foundation. However, do not get stuck on complex <em>Rotational Motion</em> problems involving multiple pulleys and slipping. In NEET, the questions are usually formula-based (e.g., Moment of Inertia of standard bodies). Focus more on <em>Kinematics</em>, <em>Laws of Motion</em>, and <em>Work, Power, Energy</em>.</p>

            <h3>2. The "3-Step" Problem Solving Algorithm</h3>
            <p>Students often read a question and freeze. To overcome this, use a mechanical approach:</p>
            <ul>
                <li><strong>Step 1: Data Extraction.</strong> Read the question and immediately write down given variables (u=0, a=5, t=10) with units.</li>
                <li><strong>Step 2: Formula Mapping.</strong> Identify which formula connects these variables. (e.g., s = ut + 1/2at²).</li>
                <li><strong>Step 3: Unit Check & Calculation.</strong> Ensure all units are in SI (meters, seconds, kg) before putting them into the formula. 40% of silly mistakes happen here.</li>
            </ul>

            <h3>3. Mastering Graph-Based Questions</h3>
            <p>NEET loves graphs. You will consistently find 4-5 questions based purely on slope (differentiation) or area under the curve (integration).</p>
            <ul>
                <li><strong>Slope (m = tan&theta;):</strong> In a V-T graph, the slope is Acceleration. In a Distance-Time graph, it is Speed.</li>
                <li><strong>Area:</strong> The area under a V-T graph gives Displacement. The area under an F-S graph gives Work Done.</li>
            </ul>
            <p>Understand the physical significance of slope and area for every chapter, from Kinematics to Thermodynamics.</p>

            <h3>4. Theoretical Questions: The Silent Killers</h3>
            <p>Recently, the trend has shifted towards statement-based theoretical questions, especially in chapters like <em>Magnetism and Matter</em> and <em>Properties of Solids</em>.</p>
            <p>Read the "Points to Ponder" and "Summary" sections of NCERT Physics. Questions about diamagnetism/paramagnetism, hysteresis loops, and logic gates are purely theoretical and require zero calculation time.</p>

            <h3>5. Thermodynamics & KTG</h3>
            <p>This unit overlaps significantly with Chemistry (States of Matter and Thermodynamics). If you study this well in Physics, you get a "Buy One, Get One Free" advantage. Focus on:</p>
            <ul>
                <li>First Law of Thermodynamics (Sign convention is opposite to Chemistry!).</li>
                <li>Carnot Engine efficiency (Efficiency = 1 - T2/T1).</li>
                <li>Degrees of Freedom in KTG.</li>
            </ul>

            <h3>6. Approximation Techniques</h3>
            <p>In NEET, options are often spaced far apart (e.g., A. 9.8, B. 98, C. 0.98, D. 980). You do not need precise calculation.</p>
            <ul>
                <li>Take <code>g = 10</code> instead of 9.8.</li>
                <li>Take <code>&pi;² &approx; 10</code>.</li>
                <li>Take <code>&radic;2 = 1.4</code> and <code>&radic;3 = 1.7</code>.</li>
            </ul>
            <p>Using these approximations can save you 30-40 seconds per question, which adds up to 10-15 minutes of extra time in the exam.</p>

            <hr>
            <p class="text-muted"><em>Physics is not about IQ; it is about EQ (Emotional Quotient). Don't let the fear of a tough calculation paralyze you. Skip the 5 hardest questions and secure the 40 easy ones to hit your target score.</em></p>
        """
    },

    # CA Articles
    "ca-roadmap": {
        "title": "Chartered Accountancy: The Ultimate Roadmap from Foundation to Final",
        "content": """
            <p class="lead">Chartered Accountancy (CA) is not just a course; it is a test of character. It is widely regarded as one of the toughest professional examinations in the world, with a pass percentage that often hovers in the single digits. The journey from a student to a member of the ICAI is a marathon, not a sprint. Here is your complete strategic roadmap to navigating this rigorous path.</p>
            
            <hr>

            <h3>1. CA Foundation: Building the Base</h3>
            <p>The entry-level test might seem easy compared to what follows, but it filters out nearly 70% of applicants. The syllabus comprises four papers:</p>
            <ul>
                <li><strong>Principles and Practice of Accounting:</strong> This is your stronghold. Aim for 80+ marks here to aggregate your total score. Focus on Bank Reconciliation Statements (BRS), Consignment, and Final Accounts.</li>
                <li><strong>Business Laws & BCR:</strong> Law is new for 12th-grade pass-outs. The challenge is the technical language. Do not write in layman's English; use legal terminology (e.g., "Void ab initio," "Consideration").</li>
                <li><strong>Business Mathematics, LR & Statistics:</strong> This is the graveyard for non-math students. Focus heavily on Logical Reasoning (20 marks) and Statistics (40 marks) if Calculus scares you. Time value of money is the most critical chapter.</li>
                <li><strong>Business Economics:</strong> A high-scoring objective paper. Read the ICAI module line-by-line.</li>
            </ul>

            <h3>2. CA Intermediate: The Real Filter</h3>
            <p>This is where the syllabus expands by 500%. It consists of two groups with four papers each. The jump in difficulty from Foundation to Inter is massive.</p>
            <h4>Group 1 Strategy</h4>
            <p><strong>Accounting</strong> requires mastery of Accounting Standards (AS). <strong>Corporate & Other Laws</strong> is vast; focus on the Companies Act sections. <strong>Costing</strong> is a practical paper; practice formatting your answers correctly. <strong>Taxation</strong> (Income Tax + GST) is the toughest paper for many because of the sheer volume of amendments. Prioritize GST (40 marks) as it is smaller and more scoring.</p>
            
            <h4>Group 2 Strategy</h4>
            <p><strong>Advanced Accounts</strong> focuses on complicated standards and partnership/consolidation. <strong>Auditing & Assurance</strong> is a theory-heavy paper where keywords matter more than length. <strong>EIS-SM</strong> and <strong>FM-Eco</strong> are the final hurdles; Strategic Management (SM) is your savior in that paper.</p>

            <h3>3. Articleship: The Practical Grinds</h3>
            <p>After clearing either or both groups of Intermediate, you enter 3 years (now 2 years under the new scheme) of practical training. Do not opt for "Dummy Articleship." The exposure you get in Auditing, Tax Filing, and Corporate Laws during this period is what helps you solve case-study-based questions in CA Final. Treat your principal as your mentor.</p>

            <h3>4. CA Final: The Ultimate Challenge</h3>
            <p>The Final level tests your ability to apply concepts to real-world scenarios. It is no longer about "What is Section 144?"; it is about "How does Section 144 apply to this bankrupt company?"</p>
            <ul>
                <li><strong>Financial Reporting (FR):</strong> Entirely based on Ind AS. This is the longest paper. Speed is key.</li>
                <li><strong>Strategic Financial Management (SFM):</strong> The most scoring practical paper. Master Forex and Derivatives.</li>
                <li><strong>Audit & Law:</strong> Professional Ethics is a small chapter but carries 12-16 marks. Never skip it.</li>
                <li><strong>Direct & Indirect Tax:</strong> These are open-book exams in terms of volume, but the questions are tricky. Linking different provisions is essential.</li>
            </ul>

            <h3>5. The Golden Rules of Survival</h3>
            <ul>
                <li><strong>ICAI Study Material is Bible:</strong> 90% of questions come directly from the ICAI Practice Manual (PM) and Study Material (SM). Do not ignore them for expensive coaching books.</li>
                <li><strong>Mock Tests:</strong> You must write at least 3 full-syllabus mock tests before the actual exam. The 3-hour timer creates a pressure that you need to get used to.</li>
                <li><strong>Revision Strategy:</strong> If you cannot revise the syllabus in the 1.5 days before the exam, you will not clear it. Make concise "LDR" (Last Day Revision) notes during your prep.</li>
            </ul>

            <hr>
            <p class="text-muted"><em>The prefix "CA" before your name commands respect across the globe. The sleepless nights, the missed festivals, and the stress are the price you pay for that two-letter prefix. Keep going.</em></p>
        """
    },

    # Teaching Exam Articles
    "ctet-cdp": {
        "title": "CTET 2026: Mastering Child Development & Pedagogy (CDP)",
        "content": """
            <p class="lead">Child Development and Pedagogy (CDP) is the heart of the Central Teacher Eligibility Test (CTET). It carries 30 marks directly in Paper 1 and Paper 2, but its concepts are also applied in the Pedagogy sections of Math, Science, Social Studies, and Languages. If you master CDP, you effectively prepare for 90 marks of the exam. Here is your comprehensive guide to the theories and concepts that appear every year.</p>
            
            <hr>

            <h3>1. Jean Piaget: Theory of Cognitive Development</h3>
            <p>Piaget is the most frequently asked theorist in CTET. He viewed children as "Little Scientists" who actively construct their understanding of the world.</p>
            <ul>
                <li><strong>Schema:</strong> The building blocks of knowledge.</li>
                <li><strong>Assimilation:</strong> Fitting new information into existing schemas (e.g., calling a cat a "dog").</li>
                <li><strong>Accommodation:</strong> Modifying existing schemas to fit new information (e.g., realizing cats meow and dogs bark, so they are different).</li>
            </ul>
            <h4>The 4 Stages of Development:</h4>
            <ul>
                <li><strong>Sensorimotor (0-2 Years):</strong> Object Permanence develops. Learning through senses and motor actions.</li>
                <li><strong>Pre-Operational (2-7 Years):</strong> Egocentrism (cannot see others' perspective) and Animism (thinking toys are alive). Lack of Conservation.</li>
                <li><strong>Concrete Operational (7-11 Years):</strong> Logic begins for concrete objects. Mastery of Conservation, Classification, and Seriation. Reversibility of thought develops.</li>
                <li><strong>Formal Operational (11+ Years):</strong> Abstract thinking, hypothetical-deductive reasoning, and problem-solving.</li>
            </ul>

            <h3>2. Lev Vygotsky: Socio-Cultural Theory</h3>
            <p>Unlike Piaget, Vygotsky believed that learning is a social activity. His theory emphasizes three key pillars:</p>
            <ul>
                <li><strong>Social Interaction:</strong> Children learn through dialogue with more knowledgeable peers or adults.</li>
                <li><strong>Culture:</strong> Cultural tools (language, counting systems) shape cognitive development.</li>
                <li><strong>Language:</strong> Private Speech (talking to oneself) guides cognitive development.</li>
            </ul>
            <h4>Key Concepts:</h4>
            <ul>
                <li><strong>ZPD (Zone of Proximal Development):</strong> The gap between what a child can do alone and what they can do with help.</li>
                <li><strong>Scaffolding:</strong> Temporary support provided by an adult (MKO - More Knowledgeable Other) to help the child cross the ZPD. Examples: Hints, cues, half-solved problems.</li>
            </ul>

            <h3>3. Lawrence Kohlberg: Stages of Moral Development</h3>
            <p>Kohlberg expanded on Piaget's ideas to study how we develop a sense of right and wrong. He famously used the "Heinz Dilemma."</p>
            <ul>
                <li><strong>Level 1: Pre-Conventional (4-10 Years):</strong> Morality is external.
                    <br><em>Stage 1:</em> Obedience & Punishment (Avoid punishment).
                    <br><em>Stage 2:</em> Individualism & Exchange ("What's in it for me?").</li>
                <li><strong>Level 2: Conventional (10-13 Years):</strong> Social norms matter.
                    <br><em>Stage 3:</em> Good Boy-Nice Girl (Seeking social approval).
                    <br><em>Stage 4:</em> Law & Order (Obeying rules to maintain society).</li>
                <li><strong>Level 3: Post-Conventional (13+ Years):</strong> Universal ethics.
                    <br><em>Stage 5:</em> Social Contract (Rules can change for the greater good).
                    <br><em>Stage 6:</em> Universal Ethical Principles (Human rights above law).</li>
            </ul>

            <h3>4. Inclusive Education (5 Marks Guaranteed)</h3>
            <p>Inclusive education means teaching all children—regardless of physical, intellectual, social, or linguistic differences—under one roof. It moves away from "Segregation" or "Integration."</p>
            <p><strong>Key Principles:</strong> Zero rejection, individualized education plans (IEP), and flexible curriculum. Teachers must act as facilitators, not dictators.</p>

            <h3>5. Learning Disabilities</h3>
            <p>You will always find 1-2 questions matching disabilities to their symptoms:</p>
            <ul>
                <li><strong>Dyslexia:</strong> Difficulty in reading (e.g., reading 'saw' as 'was' or 'b' as 'd').</li>
                <li><strong>Dysgraphia:</strong> Difficulty in writing (illegible handwriting, poor spacing).</li>
                <li><strong>Dyscalculia:</strong> Difficulty in mathematics and calculation.</li>
                <li><strong>Dysphasia:</strong> Difficulty in language comprehension.</li>
                <li><strong>ADHD (Attention Deficit Hyperactivity Disorder):</strong> Difficulty focusing, impulsivity, and inability to sit still.</li>
            </ul>

            <h3>6. NCF 2005 & NEP 2020</h3>
            <p>The National Curriculum Framework (NCF) 2005 is the guiding light for CTET pedagogy.</p>
            <ul>
                <li>Learning should be shifted away from rote methods.</li>
                <li>Curriculum must go beyond textbooks.</li>
                <li>Examination system should be more flexible (Continuous and Comprehensive Evaluation - CCE).</li>
                <li>Learning must be connected to real life outside the school.</li>
            </ul>

            <h3>7. Motivation & Learning</h3>
            <p>Understanding the difference between <strong>Intrinsic Motivation</strong> (doing it for the joy of learning) and <strong>Extrinsic Motivation</strong> (doing it for rewards/marks) is crucial. Maslow's Hierarchy of Needs is also a frequent topic, emphasizing that physiological and safety needs must be met before a child can focus on cognitive needs.</p>

            <hr>
            <p class="text-muted"><em>Pedagogy is about "How to Teach" rather than "What to Teach." In the exam, always choose the option that makes the child active, independent, and curious. Eliminate options that suggest rote memorization, punishment, or labeling children.</em></p>
        """
    },
    # Defense Articles
    "preparation-strategy": {
        "title": "CDS 2026: The Ultimate 6-Month Preparation Blueprint",
        "content": """
            <p class="lead">The Combined Defence Services (CDS) examination is not just a test of knowledge; it is a test of personality, discipline, and time management. Conducted by UPSC twice a year, it requires a strategy that goes beyond rote learning. Whether you are aiming for IMA, INA, AFA, or OTA, this 6-month roadmap is your guide to earning the uniform.</p>
            
            <hr>

            <h3>Phase 1: Foundation Building (Months 1-2)</h3>
            <p>The first two months are about building a base. Do not touch advanced books yet.</p>
            <ul>
                <li><strong>English:</strong> Start reading 'The Hindu' or 'The Indian Express' editorial page daily. This is non-negotiable. It improves your vocabulary and reading speed for comprehension passages. For grammar, pick up <em>Wren & Martin</em> and finish the chapters on Parts of Speech, Tenses, and Prepositions.</li>
                <li><strong>General Knowledge (GK):</strong> Start with NCERTs. Read Class 9th and 10th Science (Physics, Chemistry, Biology) and Class 11th & 12th Geography. Science alone accounts for 30+ questions in the GK paper.</li>
                <li><strong>Mathematics (For IMA/AFA/INA):</strong> Focus on Arithmetic. Complete Number Systems, Time & Work, Percentage, and Profit & Loss. Your speed must be high here.</li>
            </ul>

            <h3>Phase 2: Core Competency (Months 3-4)</h3>
            <p>Now, shift gears to standard reference books and specialized topics.</p>
            <ul>
                <li><strong>Polity:</strong> Read <em>M. Laxmikanth</em>. You do not need to read the whole book. Focus on Fundamental Rights, DPSP, President, Parliament, and Emergency Provisions. These 5 chapters cover 80% of Polity questions.</li>
                <li><strong>Geography:</strong> Move to <em>G.C. Leong</em> (Part 1 for Physical Geography). Understand concepts like Cyclones, Ocean Currents, and Wind Systems. Map work is crucial—practice marking straits, mountain ranges, and rivers daily.</li>
                <li><strong>History:</strong> Focus on Modern History (Spectrum by Rajiv Ahir). Ancient and Medieval history have a low return on investment; stick to the "Themes in Indian History" NCERTs for them.</li>
                <li><strong>Mathematics:</strong> This is the time for Advanced Maths. Trigonometry, Geometry, and Mensuration carry the maximum weightage. Memorize standard identities and theorems.</li>
            </ul>

            <h3>Phase 3: The "Kill" Phase (Month 5)</h3>
            <p>This month is dedicated to <strong>Previous Year Questions (PYQs)</strong>. This is the secret sauce.</p>
            <ul>
                <li><strong>English:</strong> Solve last 10 years' papers. You will notice that Antonyms/Synonyms and Ordering of Sentences patterns repeat frequently.</li>
                <li><strong>GK:</strong> Analyze the trend. If UPSC asked about a specific vitamin deficiency in 2024, they might ask about its source in 2026. This is called "lateral reading."</li>
                <li><strong>Current Affairs:</strong> Do not rely on daily videos. Pick up a monthly compilation (like Pratiyogita Darpan or any reputable coaching magazine) and cover the last 6 months of Defense Exercises, Awards, Books, and Government Schemes.</li>
            </ul>

            <h3>Phase 4: Revision & Mocks (Month 6)</h3>
            <p>In the final month, stop reading new material.</p>
            <ul>
                <li><strong>Mock Tests:</strong> Attempt at least 10 full-length mocks. Sit for the exam at the actual time (e.g., English at 9 AM, GK at 12 PM). This biological clock training is essential to avoid lethargy during the GK paper.</li>
                <li><strong>Science Revision:</strong> Revise your notes on diseases, vitamins, optics (Physics), and chemical formulas. Science questions are the most factual and easiest to score.</li>
                <li><strong>Maths Formulas:</strong> Keep a "Formula Sheet" for Mensuration (2D & 3D) and revise it every morning.</li>
            </ul>

            <h3>Subject-Wise Golden Rules</h3>
            
            <h4>1. English (100 Marks / 120 Questions)</h4>
            <p><strong>Target: 70+ Marks.</strong><br>
            English is the scoring subject. If you score below 60 here, clearing the cutoff becomes mathematically difficult. Focus on "S1-S6" (Ordering of Sentences) and Cloze Tests. Avoid guessing in Antonyms/Synonyms if you are clueless.</p>

            <h4>2. General Knowledge (100 Marks / 120 Questions)</h4>
            <p><strong>Target: 40-50 Marks.</strong><br>
            UPSC GK is notoriously tough. Do not try to answer everything. Physics, Chemistry, Biology, Polity, and Geography are the "Static 5" that will help you clear the sectional cutoff. Economics and Current Affairs can be risky; attempt them only if sure.</p>

            <h4>3. Mathematics (100 Marks / 100 Questions)</h4>
            <p><strong>Target: 60+ Marks.</strong><br>
            Speed is the enemy here. You have 1 minute per question. Use options to solve questions (Substitution method) wherever possible, especially in Trigonometry and Algebra. If a question takes more than 2 minutes, skip it immediately.</p>

            <hr>
            <p class="text-muted"><em>"The more you sweat in peace, the less you bleed in war." Treat this preparation as your peacetime training. Consistency of 6 hours a day is far better than studying 14 hours once a week. Good luck, future officers.</em></p>
        """
    },
    "cds-2026-dates": {
        "title": "CDS 1 2026 Notification: Exam Dates, Eligibility & Age Limit",
        "content": """
            <p class="lead">The Combined Defence Services (CDS) Examination is the gateway for graduates to join the Indian Armed Forces as Commissioned Officers. Conducted twice a year by the Union Public Service Commission (UPSC), CDS 1 2026 is one of the most anticipated defense exams. Below is the complete breakdown of the notification, important dates, and strict eligibility criteria you must know before applying.</p>
            
            <hr>

            <h3>1. CDS 1 2026 Important Dates (Tentative)</h3>
            <p>Based on the UPSC Annual Calendar trends, the official notification for CDS 1 2026 is expected to be released in December 2025. Mark these dates in your calendar:</p>
            <table class="table table-bordered table-hover mt-3">
                <thead class="table-dark">
                    <tr>
                        <th>Event</th>
                        <th>Tentative Date</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Notification Release Date</strong></td>
                        <td>20th December 2025</td>
                    </tr>
                    <tr>
                        <td><strong>Online Application Start</strong></td>
                        <td>20th December 2025</td>
                    </tr>
                    <tr>
                        <td><strong>Last Date to Apply</strong></td>
                        <td>9th January 2026 (till 6:00 PM)</td>
                    </tr>
                    <tr>
                        <td><strong>Admit Card Release</strong></td>
                        <td>March 2026 (3 weeks before exam)</td>
                    </tr>
                    <tr>
                        <td><strong>CDS 1 2026 Exam Date</strong></td>
                        <td><strong>April 2026 (Sunday)</strong></td>
                    </tr>
                    <tr>
                        <td><strong>Result Declaration</strong></td>
                        <td>May 2026</td>
                    </tr>
                </tbody>
            </table>

            <h3>2. Detailed Age Limit & Marital Status</h3>
            <p>The age criteria for CDS are extremely strict. Candidates must be <strong>Unmarried</strong> (except for certain departmental candidates). The age is calculated as of the commencement of the course (January 2027).</p>
            <ul>
                <li><strong>Indian Military Academy (IMA):</strong> 19 to 24 Years. Born not earlier than 2nd Jan 2003 and not later than 1st Jan 2008.</li>
                <li><strong>Indian Naval Academy (INA):</strong> 19 to 24 Years. Born not earlier than 2nd Jan 2003 and not later than 1st Jan 2008.</li>
                <li><strong>Air Force Academy (AFA):</strong> 20 to 24 Years. Born not earlier than 2nd Jan 2003 and not later than 1st Jan 2007. (Upper age limit relaxable up to 26 years for candidates holding a valid Commercial Pilot License issued by DGCA).</li>
                <li><strong>Officers' Training Academy (OTA - Men & Women):</strong> 19 to 25 Years. Born not earlier than 2nd Jan 2002 and not later than 1st Jan 2008.</li>
            </ul>
            <p><em>Note: Date of birth entered must match exactly with the Matriculation/Secondary School Examination Certificate.</em></p>

            <h3>3. Educational Qualification</h3>
            <p>Your degree determines which academy you can apply for:</p>
            <ul>
                <li><strong>For I.M.A. and OTA:</strong> A Degree of a recognized University or equivalent (Any Stream - Arts, Commerce, Science, B.Tech, etc.).</li>
                <li><strong>For Indian Naval Academy (INA):</strong> Degree in Engineering from a recognized University/Institution (B.E. / B.Tech).</li>
                <li><strong>For Air Force Academy (AFA):</strong> Degree of a recognized University (with Physics and Mathematics at 10+2 level) OR Bachelor of Engineering.</li>
            </ul>
            <p><strong>Final Year Students:</strong> Candidates appearing in the final year/semester degree exam can also apply, provided they do not have any present backlog up to the last semester/year.</p>

            <h3>4. Vacancy Distribution</h3>
            <p>While the exact number varies with every notification, the tentative distribution is usually around 340-350 seats:</p>
            <ul>
                <li><strong>IMA, Dehradun:</strong> ~100 posts</li>
                <li><strong>INA, Ezhimala:</strong> ~32 posts</li>
                <li><strong>AFA, Hyderabad:</strong> ~32 posts</li>
                <li><strong>OTA, Chennai (Men):</strong> ~170 posts</li>
                <li><strong>OTA, Chennai (Women):</strong> ~17 posts</li>
            </ul>

            <h3>5. Scheme of Examination</h3>
            <p>The exam pattern differs for OTA and permanent commission academies (IMA/INA/AFA).</p>
            <h4>For IMA, INA, and AFA:</h4>
            <ul>
                <li><strong>English:</strong> 100 Marks (2 Hours)</li>
                <li><strong>General Knowledge:</strong> 100 Marks (2 Hours)</li>
                <li><strong>Elementary Mathematics:</strong> 100 Marks (2 Hours)</li>
                <li><strong>Total:</strong> 300 Marks</li>
            </ul>
            <h4>For OTA (Officers' Training Academy):</h4>
            <ul>
                <li><strong>English:</strong> 100 Marks (2 Hours)</li>
                <li><strong>General Knowledge:</strong> 100 Marks (2 Hours)</li>
                <li><strong>Total:</strong> 200 Marks (No Math paper)</li>
            </ul>
            <p><em>Negative Marking:</em> There is a penalty of 1/3rd marks (0.33) for every wrong answer.</p>

            <h3>6. SSB Interview & Medicals</h3>
            <p>Clearing the written exam is just step one. Shortlisted candidates are called for the <strong>Services Selection Board (SSB)</strong> interview, which is a 5-day process testing Intelligence and Personality.</p>
            <ul>
                <li><strong>Stage I:</strong> Screening Test (OIR + PPDT).</li>
                <li><strong>Stage II:</strong> Psychology Tests, GTO Tasks, and Personal Interview.</li>
            </ul>
            <p>Recommended candidates then undergo a rigorous Medical Examination. Only those who are medically fit and make it to the All India Merit List join the prestigious academies.</p>

            <hr>
            <p class="text-muted"><em>The competition is fierce, but the reward is a life less ordinary. Start your preparation early, focus on your fitness, and ensure your documents are in order for the application process.</em></p>
        """
    },
    "paper-2-tips": {
        "title": "CAPF AC 2026: The Ultimate Blueprint to Score 90+ in Paper 2",
        "content": """
            <p class="lead">Paper 2 (General Studies, Essay, and Comprehension) is the "Game Changer" of the CAPF Assistant Commandant examination. While Paper 1 is objective and predictable, Paper 2 is subjective and tests your analytical depth. Most candidates fail to clear the sectional cutoff, while toppers use this paper to skyrocket their merit ranking. Here is the definitive strategy to cross the 90-mark barrier.</p>
            
            <hr>

            <h3>1. The Time Management Crisis</h3>
            <p>The biggest challenge in Paper 2 is not <em>knowledge</em>, but <em>time</em>. You have 3 hours to write 4 Essays, 2 Arguments, 2 Reports, 1 Précis, 1 Comprehension, and Grammar questions. A single slip-up can leave 20 marks unattempted.</p>
            <p><strong>The Golden Timeline:</strong></p>
            <ul>
                <li><strong>Essays (4 x 18 mins):</strong> 72 Minutes.</li>
                <li><strong>Arguments (2 x 15 mins):</strong> 30 Minutes.</li>
                <li><strong>Reports (2 x 10 mins):</strong> 20 Minutes.</li>
                <li><strong>Grammar:</strong> 15 Minutes (Do this first or right after arguments).</li>
                <li><strong>Comprehension & Précis:</strong> 40 Minutes.</li>
                <li><strong>Buffer:</strong> 3 Minutes.</li>
            </ul>

            <h3>2. Mastering the Essay (80 Marks)</h3>
            <p>You must write 4 essays out of 6 options (300 words each). Do not treat this like a college exam.</p>
            <ul>
                <li><strong>Structure is King:</strong> Every essay must have an <strong>Introduction</strong> (Define the topic or start with a quote/data), a <strong>Body</strong> (Social, Political, Economic, International dimensions), and a <strong>Conclusion</strong> (Futuristic and optimistic).</li>
                <li><strong>Data Dump:</strong> An essay without data is just an opinion. If you are writing about "Women Safety," quote NCRB data. If writing about "Economy," quote the latest GDP growth rate or IMF projection.</li>
                <li><strong>Language:</strong> Keep sentences short. Avoid flowery Shashi Tharoor-style English. The examiner values clarity and administrative thought process over vocabulary.</li>
            </ul>

            <h3>3. Writing "For and Against" Arguments (40 Marks)</h3>
            <p>This section tests your neutrality. You are a future officer; you cannot be biased.</p>
            <ul>
                <li><strong>Format:</strong> Strictly use bullet points. Write 5 strong points "For" the motion and 5 strong points "Against" the motion.</li>
                <li><strong>The Introduction:</strong> A one-line intro defining the core issue is sufficient.</li>
                <li><strong>Tone:</strong> Be objective. Instead of saying "The government failed," say "There have been implementation gaps in the policy."</li>
                <li><strong>Conclusion:</strong> A balanced conclusion is mandatory. It should bridge the gap between the opposing views.</li>
            </ul>

            <h3>4. Report Writing: Be a Journalist (20 Marks)</h3>
            <p>Reports are factual accounts of an event. Do not give suggestions or opinions here.</p>
            <ul>
                <li><strong>The Header:</strong> Format is crucial.
                    <br><em>Headline: Operation Kaveri Evacuates Indians</em>
                    <br><em>XYZ, New Delhi, 26th April</em></li>
                <li><strong>Past Tense:</strong> Reports are always written in the past tense because the event has already happened.</li>
                <li><strong>Structure:</strong>
                    <br><em>Para 1:</em> What, Where, When, Who?
                    <br><em>Para 2:</em> Details, Government response, Eye-witness account.
                    <br><em>Para 3:</em> Future course of action or current status.</li>
            </ul>

            <h3>5. Précis Writing: The Art of Brevity (15 Marks)</h3>
            <p>You must compress a passage to 1/3rd of its length. This is technically the toughest part.</p>
            <ul>
                <li><strong>The Box Rule:</strong> UPSC provides a grid sheet (one word per box). Adhere to it strictly.</li>
                <li><strong>Own Words:</strong> Never copy sentences from the original passage. Read, understand, and rewrite in your own simple language.</li>
                <li><strong>No Title:</strong> Do not give a title unless explicitly asked (usually not asked in CAPF).</li>
            </ul>

            <h3>6. Grammar: The Mathematical Marks (25 Marks)</h3>
            <p>This is the only section where you can score 25/25. It includes:</p>
            <ul>
                <li><strong>Active-Passive Voice</strong></li>
                <li><strong>Direct-Indirect Speech</strong></li>
                <li><strong>Transformation of Sentences</strong> (Simple to Complex, Positive to Comparative)</li>
                <li><strong>Phrasal Verbs</strong> (Make sentences to show meaning)</li>
            </ul>
            <p><strong>Strategy:</strong> Practice the last 10 years of CAPF and CDS grammar questions. The concepts (like "Hardly... when", "No sooner... than") repeat every single year.</p>

            <h3>7. Reading Comprehension (20 Marks)</h3>
            <p>Do not use outside knowledge. If the passage says "The sun rises in the West," then for your answer, the sun rises in the West. Stick strictly to the text provided. Answers should be concise and direct.</p>

            <hr>
            <p class="text-muted"><em>Paper 2 requires stamina. Your hand will hurt, and your mind will fatigue by the 2nd hour. The only way to survive is to practice writing 3 full-length tests on Sundays in the month leading up to the exam.</em></p>
        """
    },
    "cpo-guide": {
        "title": "SSC CPO 2026: The Complete Guide to Physical (PET/PST) & Medical Standards",
        "content": """
            <p class="lead">The Staff Selection Commission (SSC) Central Police Organization (CPO) exam is unique among government competitive exams. Unlike banking or civil services where intellectual capability is the sole criteria, CPO demands a perfect balance of mental agility and physical robustness. It is the gateway to becoming a Sub-Inspector (SI) in the prestigious Delhi Police and CAPFs (BSF, CRPF, CISF, ITBP, SSB). However, nearly 40% of candidates who clear the written exam fail the physical stage. Here is detailed scrutiny of the standards you must meet.</p>
            
            <hr>

            <h3>1. Stage 1: Physical Standard Test (PST)</h3>
            <p>Before you run, you are measured. The PST is strictly objective. If you fall short by even 0.5 cm in height or chest expansion, you are disqualified immediately. There are no appeals.</p>
            
            <h4>For Male Candidates:</h4>
            <ul>
                <li><strong>General / OBC / SC:</strong> Minimum Height: <strong>170 cm</strong>. Chest: <strong>80 cm</strong> (Unexpanded) and <strong>85 cm</strong> (Expanded). A minimum expansion of 5 cm is mandatory.</li>
                <li><strong>Hill Areas (Garhwal, Kumaon, Himachal, J&K, North East):</strong> Minimum Height: <strong>165 cm</strong>. Chest standards remain the same (80-85 cm).</li>
                <li><strong>Scheduled Tribes (ST):</strong> Minimum Height: <strong>162.5 cm</strong>. Chest: <strong>77-82 cm</strong>.</li>
            </ul>

            <h4>For Female Candidates:</h4>
            <ul>
                <li><strong>General / OBC / SC:</strong> Minimum Height: <strong>157 cm</strong>. There is no chest measurement for female candidates.</li>
                <li><strong>Hill Areas:</strong> Minimum Height: <strong>155 cm</strong>.</li>
                <li><strong>Scheduled Tribes (ST):</strong> Minimum Height: <strong>154 cm</strong>.</li>
            </ul>
            <p><strong>Weight:</strong> For both genders, weight must be proportionate to height and age as per medical standards. Being overweight is a temporary rejection (TR), but it creates issues during the endurance test.</p>

            <h3>2. Stage 2: Physical Endurance Test (PET)</h3>
            <p>This is the test of your stamina and explosive power. The events are mandatory and qualifying in nature.</p>
            
            <h4>Male Candidates Events:</h4>
            <ul>
                <li><strong>100 Meters Race:</strong> Must be completed in <strong>16 seconds</strong>. This tests pure speed.</li>
                <li><strong>1.6 Km Race:</strong> Must be completed in <strong>6.5 minutes</strong>. This tests endurance. Most rejections happen here.</li>
                <li><strong>Long Jump:</strong> <strong>3.65 meters</strong> (approx 12 feet). You get 3 chances. Foul line mistakes are common.</li>
                <li><strong>High Jump:</strong> <strong>1.2 meters</strong> (approx 4 feet). You get 3 chances. Using the "Scissors" or "Phosphory Flop" technique helps.</li>
                <li><strong>Shot Put (16 Lbs):</strong> <strong>4.5 meters</strong>. You get 3 chances. This is generally the easiest event for most candidates.</li>
            </ul>

            <h4>Female Candidates Events:</h4>
            <ul>
                <li><strong>100 Meters Race:</strong> Must be completed in <strong>18 seconds</strong>.</li>
                <li><strong>800 Meters Race:</strong> Must be completed in <strong>4 minutes</strong>. Pacing is crucial here.</li>
                <li><strong>Long Jump:</strong> <strong>2.7 meters</strong> (9 feet). 3 Chances given.</li>
                <li><strong>High Jump:</strong> <strong>0.9 meters</strong> (3 feet). 3 Chances given.</li>
            </ul>

            <h3>3. Stage 3: Detailed Medical Examination (DME)</h3>
            <p>Once you clear Paper 2 (English), you face the Medical Board. The standards are military-grade.</p>
            
            <h4>Eye Sight (Visual Standards):</h4>
            <ul>
                <li><strong>Visual Acuity:</strong> The better eye must be <strong>6/6</strong> and the worse eye <strong>6/9</strong>. This must be achieved <strong>without glasses</strong>.</li>
                <li><strong>Color Blindness:</strong> Candidates must not have color blindness (CP-III by Ishihara plates). This is a permanent rejection.</li>
                <li><strong>LASIK Surgery:</strong> Strictly prohibited. If a candidate is found to have undergone corrective eye surgery, they are disqualified.</li>
            </ul>

            <h4>Common Rejection Grounds:</h4>
            <ul>
                <li><strong>Knock Knee:</strong> When standing straight with ankles touching, the knees should not touch each other.</li>
                <li><strong>Flat Foot:</strong> The sole of the foot must have a visible arch. Wet footprint tests are used to check this.</li>
                <li><strong>Varicose Veins:</strong> Swollen, twisted veins in the legs (usually behind the calf) are a ground for rejection.</li>
                <li><strong>Tattoos:</strong> Tattoos depicting religious symbols or names are permitted on the inner face of the forearm (non-saluting arm). However, the size must be less than 1/4th of the particular body part.</li>
            </ul>

            <h3>4. Preparation Strategy for Physicals</h3>
            <p>Do not wait for Paper 1 results to start running. Shin splints (pain in the lower leg) are common among beginners who run too hard too soon. Start with a slow jog for 20 minutes daily. For high jump and long jump, technique matters more than power. Practice on a proper sandpit to avoid ankle injuries.</p>

            <hr>
            <p class="text-muted"><em>Becoming a Sub-Inspector involves commanding a platoon and maintaining law and order in volatile situations. The rigorous physical standards ensure that only those with the grit to serve the nation make the cut. Train hard.</em></p>
        """
    },
    # --- BROKEN LINK FIXES & NEW CONTENT ---
    
    "jee-pyq": {
        "title": "Importance of JEE Previous Year Questions (2015-2025)",
        "content": "<p>Solving PYQs is the single most effective strategy for JEE. Trends show that 40% of concepts repeat.</p><h3>How to analyze PYQs?</h3><p>Don't just solve them. Group them chapter-wise. Identify the 'Repeated Concepts' like Rotational Motion torque problems or Thermodynamics graphs.</p><h3>Download Links</h3><p>We have compiled the last 10 years of papers. Check our Telegram channel for the direct PDF files.</p>"
    },
    "neet-bio-extracts": {
        "title": "NEET Biology NCERT Extracts: Hidden Lines Decoded",
        "content": "<p>NTA asks questions from diagram captions and summaries. This guide highlights the overlooked lines of NCERT Biology.</p><h3>Morphology Examples</h3><p>Memorize the examples of aestivation and placentation. Mnemonics are provided here.</p>"
    },
    "ca-foundation-papers": {
        "title": "CA Foundation Previous Year Papers & Mock Test Strategy",
        "content": "<p>The ICAI exams are lengthy. Practice writing answers for Law and BCR to manage time.</p><h3>Law Writing Tips</h3><p>Start with the 'Provision', then 'Facts of the Case', and finally the 'Conclusion'. Use legal terms like 'Void ab initio'.</p>"
    },
    "neet-rank-predictor-guide": {
        "title": "How to Use a NEET Rank Predictor Effectively",
        "content": "<p>Predicting your rank helps in counseling strategy. Rank depends on the difficulty level of the paper and the number of aspirants.</p><h3>Marks vs Rank</h3><p>Usually, 650+ marks guarantee a rank under 5000. 600+ marks land you around 20k-25k rank.</p>"
    },
    "ca-articleship-guide": {
        "title": "CA Articleship: Big 4 vs. Mid-Size Firms",
        "content": "<p>The biggest dilemma for a CA Intermediate student. Where should you apply?</p><h3>Big 4 Experience</h3><p>Great for audit exposure and brand value. Specific domain knowledge. Long hours.</p><h3>Mid-Size Firms</h3><p>Holistic learning. You get to do Tax, Audit, and Accounting. Better for starting your own practice later.</p>"
    },
    "age-calc": {
        "title": "Defence Exam Age Calculator: CDS, AFCAT & NDA",
        "content": "<p>Age criteria are strict in defense. A single day can disqualify you.</p><h3>CDS Age Limits</h3><p>IMA: 19-24 years. OTA: 19-25 years. The crucial date is usually 1st Jan or 1st July of the course year.</p><h3>NDA Age Limits</h3><p>16.5 to 19.5 years. Check your matriculation certificate carefully.</p>"
    },
    "syllabus-2026": {
        "title": "Exam Syllabus Updates 2026: JEE, NEET & UPSC",
        "content": "<p>Stay ahead of the curve with the latest syllabus changes for 2026.</p><h3>JEE Mains Changes</h3><p>No changes in Physics. In Chemistry, P-Block syllabus has been reduced. Solid State is removed.</p><h3>NEET Changes</h3><p>Added 'Frog' in Animal structure. Removed 'Digestion' chapter from Human Physiology.</p>"
    },
    
    # --- ADDITIONAL CONTENT TO REACH 30+ ARTICLES ---
    
    "organic-chemistry-tips": {
        "title": "5 Golden Rules to Master Organic Chemistry",
        "content": "<p>Organic chemistry is about mechanisms, not rote learning.</p><h3>1. GOC is Key</h3><p>Master Inductive, Resonance, and Hyperconjugation effects first.</p><h3>2. Reagents</h3><p>Make a list of oxidizing and reducing agents (LiAlH4, KMnO4) and their specific functions.</p>"
    },
    "inorganic-chemistry-trends": {
        "title": "Inorganic Chemistry: Periodic Table Trends",
        "content": "<p>Inorganic chemistry is high scoring. Focus on the exceptions in Ionization Energy and Atomic Radius.</p><h3>Chemical Bonding</h3><p>MOT (Molecular Orbital Theory) and VSEPR theory account for 2-3 questions in every paper.</p>"
    },
    "physics-formula-sheet": {
        "title": "Must-Know Physics Formulas for Mechanics",
        "content": "<p>Mechanics problems require formula application.</p><h3>Newton's Laws</h3><p>F=ma is just the start. Learn the impulse-momentum theorem.</p><h3>Work Power Energy</h3><p>Work-Energy theorem is the most versatile tool in Physics. Apply it when time is not given.</p>"
    },
    "history-modern-india": {
        "title": "Modern History Timeline: 1857 to 1947",
        "content": "<p>For UPSC and CDS, Modern History is crucial.</p><h3>Gandhian Era</h3><p>1915: Return of Gandhi. 1917: Champaran. 1919: Jallianwala Bagh. 1920: Non-Cooperation Movement.</p>"
    },
    "polity-articles": {
        "title": "Important Articles of Indian Constitution for CDS/NDA",
        "content": "<p>Polity is the most scoring subject in GK.</p><h3>Fundamental Rights</h3><p>Articles 12-35. Remember the writs under Article 32.</p><h3>President</h3><p>Articles 52-62. Pardoning powers and impeachment process.</p>"
    },
    "geography-maps": {
        "title": "Geography Map Work: Rivers and Mountains",
        "content": "<p>Questions on tributaries and mountain ranges are common.</p><h3>Himalayas</h3><p>Order from North to South: Karakoram, Ladakh, Zaskar, Pir Panjal.</p><h3>Peninsular Rivers</h3><p>Godavari, Krishna, Cauvery. Know their origin points.</p>"
    },
    "current-affairs-strategy": {
        "title": "How to Cover Current Affairs for Defence Exams",
        "content": "<p>Don't read everything. Focus on Defense.</p><h3>Military Exercises</h3><p>Yudh Abhyas, Malabar, Indra. Know the participating countries.</p><h3>Awards</h3><p>Param Vir Chakra, Kirti Chakra, and recent Padma awards.</p>"
    },
    "ssb-interview-guide": {
        "title": "SSB Interview: The 5-Day Procedure Explained",
        "content": "<p>SSB is a personality test.</p><h3>Day 1: Screening</h3><p>OIR test and PPDT (Picture Perception). Confidence is key in narration.</p><h3>Day 2: Psych Tests</h3><p>TAT, WAT, SRT, and Self Description. Be positive and realistic.</p>"
    },
    "afcat-strategy": {
        "title": "AFCAT 2026: Strategy for 200+ Score",
        "content": "<p>AFCAT is a speed test.</p><h3>Reasoning</h3><p>Dot situation and spatial reasoning are unique to AFCAT. Practice them well.</p><h3>English</h3><p>Idioms and phrases are asked frequently. Memorize standard lists.</p>"
    },
    "nda-vs-cds": {
        "title": "NDA vs CDS: Which Entry is Right for You?",
        "content": "<p>Both lead to the armed forces, but the entry point differs.</p><h3>NDA</h3><p>After Class 12th. Training at Khadakwasla for 3 years + 1 year at academy.</p><h3>CDS</h3><p>After Graduation. Direct entry to IMA/OTA/AFA/INA.</p>"
    },
    "banking-exam-pattern": {
        "title": "IBPS PO & Clerk: Exam Pattern & Strategy",
        "content": "<p>Banking exams are about speed and accuracy.</p><h3>Quant</h3><p>Data Interpretation (DI) is the major chunk. Master percentage and ratio calculations.</p><h3>Reasoning</h3><p>Puzzles and Seating Arrangement. Practice daily.</p>"
    },
    "ssc-cgl-guide": {
        "title": "SSC CGL 2026: Posts and Salary Structure",
        "content": "<p>The mini-IAS exam of India.</p><h3>Top Posts</h3><p>Income Tax Inspector, MEA ASO, Excise Inspector.</p><h3>Exam Pattern</h3><p>Tier 1 is qualifying. Tier 2 decides the rank. Focus on Typing and Computer knowledge too.</p>"
    },
    "clat-preparation": {
        "title": "CLAT 2026: Legal Reasoning Tips",
        "content": "<p>Law entrance requires reading speed.</p><h3>Legal Aptitude</h3><p>Do not use prior knowledge. Stick to the principle given in the passage.</p><h3>Current Affairs</h3><p>Focus on Legal news and landmark judgments.</p>"
    },
    "gate-cse-strategy": {
        "title": "GATE CSE 2026: Syllabus and High Weightage Topics",
        "content": "<p>Crack PSU jobs or M.Tech in IITs.</p><h3>Data Structures & Algo</h3><p>The most important subject. Arrays, Linked Lists, Trees, Graphs.</p><h3>Operating Systems</h3><p>Process management, Deadlocks, and Paging.</p>"
    },
    "upsc-prelims-strategy": {
        "title": "UPSC CSE Prelims: Elimination Techniques",
        "content": "<p>Prelims is becoming tougher.</p><h3>Elimination</h3><p>Extreme statements ('All', 'None', 'Only') are often wrong. Use logic to eliminate options.</p>"
    },
    # --- NEW EXAM ARTICLES (ADDED) ---
    
    "rbi-grade-b": {
        "title": "RBI Grade B 2026: The Golden Banking Career",
        "content": "<p>RBI Grade B is widely considered the most prestigious job in the Indian banking sector. The exam focuses heavily on Economics and Social Issues (ESI) and Finance & Management (FM).</p><h3>Phase 2 Strategy</h3><p>Unlike IBPS, RBI requires descriptive writing skills. You must be able to type answers on a keyboard quickly. Focus on government schemes (Pradhan Mantri yojana) and RBI circulars from the last 6 months.</p>"
    },
    "sebi-grade-a": {
        "title": "SEBI Grade A Officer: Syllabus and Strategy",
        "content": "<p>Work for the regulator of the stock market. SEBI Grade A is ideal for CA, CS, and Law graduates.</p><h3>Paper 2 Subjects</h3><p>The syllabus includes Companies Act, Costing, Commerce & Accountancy, and Economics. The difficulty level is moderate, but accuracy is key because the cutoff is usually high.</p>"
    },
    "rrb-ntpc-railways": {
        "title": "RRB NTPC: Cracking the Railway Recruitment Board Exam",
        "content": "<p>The most popular exam in India with crores of applicants.</p><h3>Mathematics & Reasoning</h3><p>These two sections make up the bulk of the score. Speed is essential. Questions are generally 10th-grade level but require shortcuts.</p><h3>General Awareness</h3><p>Focus on Static GK (Railways history, Headquarters) and current science and technology.</p>"
    },
    "cat-exam-mba": {
        "title": "CAT 2026: Gateway to IIMs and Top B-Schools",
        "content": "<p>The Common Admission Test (CAT) is a test of aptitude, not knowledge.</p><h3>VARC (Verbal Ability)</h3><p>Read Aeon Essays and editorials daily. It's about comprehension, not just grammar.</p><h3>DILR (Data Interpretation)</h3><p>The toughest section. Pick the right sets. Solving 2 out of 4 sets correctly can get you a 99 percentile.</p>"
    },
    "ugc-net-jrf": {
        "title": "UGC NET JRF: Qualifying for Assistant Professorship",
        "content": "<p>For those aspiring to teach in colleges or pursue a PhD with a stipend.</p><h3>Paper 1 (General)</h3><p>Teaching Aptitude and Research Aptitude are critical. Practice DI questions as they are mark-fetchers.</p><h3>Paper 2 (Subject)</h3><p>Deep knowledge of your Masters subject is required. Stick to standard university textbooks.</p>"
    },
    "cuet-ug-entrance": {
        "title": "CUET UG 2026: One Exam for All Central Universities",
        "content": "<p>Admission to DU, BHU, and JNU now depends on CUET.</p><h3>Domain Subjects</h3><p>The syllabus is strictly Class 12 NCERT. Do not read extra books. If you are a Science student, master your Physics, Chem, and Bio NCERTs line by line.</p><h3>General Test</h3><p>Focus on basic current affairs and logical reasoning.</p>"
    },
    "ras-rpsc-exam": {
        "title": "RPSC RAS: Strategy for Rajasthan Administrative Services",
        "content": "<p>The premier civil service of Rajasthan.</p><h3>Rajasthan GK</h3><p>This is the dealbreaker. You must know Rajasthan's Geography, History, Art & Culture, and Economy inside out. Read 'Rajasthan Adhyayan' books.</p><h3>Mains Answer Writing</h3><p>Practice writing answers in Hindi as well, as the language papers carry significant weight.</p>"
    },
    "uppsc-pcs-exam": {
        "title": "UPPSC PCS: Cracking the Uttar Pradesh Civil Services",
        "content": "<p>The syllabus overlaps 90% with UPSC, making it a great backup.</p><h3>UP Special</h3><p>Recently, optional subjects were removed and replaced with UP Special papers. Focus on UP's history, economy, and current schemes.</p><h3>Facts vs Concepts</h3><p>Unlike UPSC, UPPSC asks many factual questions (dates, names, places).</p>"
    },
    "ipmat-iim": {
        "title": "IPMAT: Integrated Programme in Management (IIM Indore/Rohtak)",
        "content": "<p>Why wait for MBA? Join IIM directly after Class 12.</p><h3>Higher Mathematics</h3><p>IPMAT asks higher-level math (Calculus, Probability, Matrices) unlike other aptitude tests. Prepare accordingly.</p><h3>Verbal Ability</h3><p>Vocabulary plays a huge role here. Learn 10 new words daily.</p>"
    },
    "gate-exam": {
        "title": "GATE 2026: Opportunities in PSUs and IITs",
        "content": "<p>Graduate Aptitude Test in Engineering is not just for M.Tech.</p><h3>PSU Recruitment</h3><p>ONGC, IOCL, NTPC recruit directly through GATE scores. You need a rank under 100 for top PSUs.</p><h3>Concepts over Rote</h3><p>GATE questions test deep conceptual understanding. Numerical questions have no options, so guessing is impossible.</p>"
    },
    "ssc-chsl-12th": {
        "title": "SSC CHSL: Best Govt Jobs after Class 12",
        "content": "<p>Secure a central government job as a Data Entry Operator or Clerk.</p><h3>Tier 1 Scoring</h3><p>Aim for 160+ to be safe. English and Reasoning are high-scoring areas.</p><h3>Typing Test</h3><p>Do not ignore typing. Many toppers fail the final skill test. Practice 15 mins daily.</p>"
    },
    "cs-executive-guide": {
        "title": "Company Secretary (CS) Executive: Module 1 vs Module 2",
        "content": "<p>CS is about Law compliance.</p><h3>Company Law</h3><p>The bible for CS. Sections of Companies Act 2013 must be on your fingertips.</p>"
    },
    
    # Default
    "default": {
        "title": "The Art of Topping Competitive Exams: A Universal Strategy",
        "content": """
            <p class="lead">Whether you are aiming for IIT JEE, NEET, CA, or UPSC, the fundamental rules of success remain the same. Competitive exams are not just a test of intelligence; they are a test of character, consistency, and strategy. While the syllabus changes, the mindset of a topper remains constant. Here is the ultimate blueprint to mastering the art of preparation.</p>
            
            <hr>

            <h3>1. The Difference: Boards vs. Competition</h3>
            <p>The biggest mistake students make is carrying their "School Mindset" into competitive prep. In school/college exams, the goal is to write <em>everything</em> you know. In competitive exams, the goal is to <em>select</em> the right answer in the shortest time.</p>
            <ul>
                <li><strong>Boards:</strong> Step-marking exists. Presentation matters. Memorization is key.</li>
                <li><strong>Competition:</strong> Only the final answer matters. Speed is currency. Application of concepts is King.</li>
            </ul>

            <h3>2. The "Reverse Engineering" Technique</h3>
            <p>Don't start by reading the first chapter of your textbook. Start by reading the <strong>Syllabus</strong> and <strong>Previous Year Questions (PYQs)</strong>.</p>
            <p>Top rankers spend the first week just analyzing the trend. If 70% of questions come from 30% of the syllabus (the Pareto Principle), you must identify that 30% immediately. For example, in Physics, Mechanics is often harder but carries less weightage than Modern Physics. Knowing this saves you months of inefficient effort.</p>

            <h3>3. The Pomodoro & Active Recall Method</h3>
            <p>Studying for 12 hours a day is useless if your brain is asleep after hour 3. Use scientific techniques:</p>
            <ul>
                <li><strong>Pomodoro Technique:</strong> Study for 50 minutes, take a strict 10-minute break. This keeps your brain in the "Alpha State" of high focus.</li>
                <li><strong>Active Recall:</strong> Do not just re-read your notes (that is passive). Close the book and force yourself to recite the page. If you struggle, that is where learning happens.</li>
                <li><strong>Spaced Repetition:</strong> Revise a topic after 1 day, then 3 days, then 7 days, then 21 days. This moves information from short-term to long-term memory.</li>
            </ul>

            <h3>4. The Mock Test Strategy</h3>
            <p>Many students avoid mock tests until they "finish the syllabus." This is a trap. The syllabus is never finished.</p>
            <ul>
                <li><strong>Attempt Strategy:</strong> Divide the paper into rounds. Round 1: Easy questions (100% sure). Round 2: Medium (50-50). Round 3: Hard (Leave or attempt at end).</li>
                <li><strong>Post-Mortem Analysis:</strong> Spending 3 hours on a test is wasted if you don't spend 4 hours analyzing it. Categorize errors into "Conceptual," "Silly Mistake," or "Lack of Time." Fix the root cause immediately.</li>
            </ul>

            <h3>5. Managing Digital Distractions</h3>
            <p>Your smartphone is the biggest enemy of your rank. The dopamine hit from a reel or notification destroys your focus span.</p>
            <p><strong>The Solution:</strong> Use apps to block social media during study hours. Turn off notifications. If you use YouTube for study, use a browser extension that blocks the "Recommended Videos" sidebar so you don't fall down a rabbit hole.</p>

            <h3>6. The Biological Engine: Sleep & Diet</h3>
            <p>Your brain consumes 20% of your body's energy. You cannot run a Ferrari on low-quality fuel.</p>
            <ul>
                <li><strong>Sleep:</strong> You need 7 hours of sleep. Memory consolidation happens during REM sleep. Pulling all-nighters actually <em>erases</em> what you studied.</li>
                <li><strong>Hydration:</strong> A 2% drop in hydration leads to a 20% drop in concentration. Keep a water bottle on your desk.</li>
                <li><strong>Sugar Crash:</strong> Avoid heavy, carb-rich lunches that make you sleepy in the afternoon. Stick to light, protein-rich meals.</li>
            </ul>

            <h3>7. Handling Failure & Burnout</h3>
            <p>You will have bad days. You will score low in mocks. You will feel like giving up. This is normal. The difference between a ranker and a dropout is that the ranker studies even on the bad days.</p>
            <p><strong>The "Why" Power:</strong> When you feel burnt out, close your eyes and visualize the result day. Visualize your parents' faces. Visualize the uniform or the college gate. Let that vision drive you back to the desk.</p>

            <hr>
            <p class="text-muted"><em>Success is the sum of small efforts, repeated day in and day out. It doesn't matter where you start; it matters where you finish. Pick up your pen and start now.</em></p>
        """
    }
}

# --- EXISTING LOGIC ---
def generate_id():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/shorten', methods=['POST'])
def shorten():
    long_url = request.json.get('url')
    short_id = generate_id()
    
    # Store in Redis: key is short_id, value is long_url
    db.set(short_id, long_url)
    
    return {"short_url": f"{request.host_url}s/{short_id}"}


@app.route('/s/<short_id>')
def start_short_path(short_id):
    # Retrieve from Redis
    if not db.exists(short_id):
        return "URL Not Found", 404
        
    session['step'] = 1
    session['target_id'] = short_id
    return redirect(url_for('interstitial'))


@app.route('/interstitial', methods=['GET', 'POST'])
def interstitial():
    step = session.get('step', 1)
    short_id = session.get('target_id')
    
    if not short_id:
        return redirect(url_for('index'))

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        correct_answer = request.form.get('correct')
        
        # Only move forward if the answer is correct
        if user_answer == correct_answer:
            session['step'] = step + 1
            if session['step'] > 5:
                return redirect(url_for('final_page'))
            return redirect(url_for('interstitial'))
        else:
            flash("Incorrect answer, please try again.")

    # Generate quiz data
    num1, num2 = random.randint(1, 10), random.randint(1, 10)
    correct = num1 + num2
    options = [correct, correct + random.randint(1, 3), correct - random.randint(1, 2)]
    random.shuffle(options)
    
    # Render the new portal-style interstitial
    return render_template('interstitial_portal.html', 
                           step=step, n1=num1, n2=num2, 
                           correct=correct, options=options)

@app.route('/final')
def final_page():
    short_id = session.get('target_id')
    # Retrieve the final URL from Redis using the stored ID
    final_url = db.get(short_id)
    return render_template('final_page.html', final_url=final_url)

@app.route('/blog/<category>/<slug>')
def blog_post(category, slug):
    # Fetch data or fall back to default if slug not found
    data = blog_data.get(slug, blog_data["default"])
    # If title missing in data, generate from slug
    title = data.get("title", slug.replace('-', ' ').title())
    content = data.get("content", "Content coming soon.")
    return render_template('blog_template.html', category=category, title=title, content=content)

@app.route('/privacy-policy')
def privacy():
    return render_template('privacy.html')

# --- NEW ROUTE FOR TERMS ---
@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash("Thank you! Your message has been sent.")
        return render_template('contact.html', success=True)
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
