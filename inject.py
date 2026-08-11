import os

file_path = r'd:\SMIT PROJECT\frontend\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Insert Feature Grid, Metrics Banner, Testimonials, FAQ, CTA before '<!-- 2. LIVE CIVIC OPERATIONS -->'
insert_index = content.find('    <!-- 2. LIVE CIVIC OPERATIONS -->')
if insert_index != -1:
    html_to_inject = '''
    <!-- NEW: FEATURE GRID -->
    <section class="section" style="background-color: var(--bg-primary);">
      <div class="container" style="max-width: 1200px; margin: 0 auto;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 1.5rem;">
          
          <div style="background: var(--bg-card); border: 1px solid var(--border); padding: 2rem; border-radius: 16px;">
            <div style="width: 40px; height: 40px; background: rgba(34, 184, 240, 0.1); border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-bottom: 1.5rem;">
              <i data-lucide="sparkles" style="color: var(--brand-primary); width: 20px; height: 20px;"></i>
            </div>
            <h3 style="font-size: 1.1rem; margin-bottom: 0.75rem;">AI complaint classification</h3>
            <p style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;">Gemini reads the description and photos of every report to detect the category, subcategory, and the exact department responsible — no forms to guess through.</p>
          </div>

          <div style="background: var(--bg-card); border: 1px solid var(--border); padding: 2rem; border-radius: 16px;">
            <div style="width: 40px; height: 40px; background: rgba(16, 185, 129, 0.1); border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-bottom: 1.5rem;">
              <i data-lucide="git-merge" style="color: var(--success); width: 20px; height: 20px;"></i>
            </div>
            <h3 style="font-size: 1.1rem; margin-bottom: 0.75rem;">Smart auto-routing</h3>
            <p style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;">Tickets are routed to the right team and officer instantly, with recommended actions and context attached, so field crews arrive prepared.</p>
          </div>

          <div style="background: var(--bg-card); border: 1px solid var(--border); padding: 2rem; border-radius: 16px;">
            <div style="width: 40px; height: 40px; background: rgba(245, 158, 11, 0.1); border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-bottom: 1.5rem;">
              <i data-lucide="clock" style="color: var(--warning); width: 20px; height: 20px;"></i>
            </div>
            <h3 style="font-size: 1.1rem; margin-bottom: 0.75rem;">SLA automation</h3>
            <p style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;">Every issue gets a priority score and a resolution deadline. Supervisors see at-risk tickets before they slip, and citizens see honest ETAs.</p>
          </div>

          <div style="background: var(--bg-card); border: 1px solid var(--border); padding: 2rem; border-radius: 16px;">
            <div style="width: 40px; height: 40px; background: rgba(34, 184, 240, 0.1); border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-bottom: 1.5rem;">
              <i data-lucide="bar-chart-2" style="color: var(--brand-primary); width: 20px; height: 20px;"></i>
            </div>
            <h3 style="font-size: 1.1rem; margin-bottom: 0.75rem;">Real-time analytics</h3>
            <p style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;">Ward-by-ward density, category trends, SLA compliance, and cost tracking — dashboards that turn operational data into decisions.</p>
          </div>

          <div style="background: var(--bg-card); border: 1px solid var(--border); padding: 2rem; border-radius: 16px;">
            <div style="width: 40px; height: 40px; background: rgba(139, 92, 246, 0.1); border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-bottom: 1.5rem;">
              <i data-lucide="shield-check" style="color: #8b5cf6; width: 20px; height: 20px;"></i>
            </div>
            <h3 style="font-size: 1.1rem; margin-bottom: 0.75rem;">Role-based access</h3>
            <p style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;">Citizen, Field Officer, Supervisor, Admin, and Super Admin — five roles with strict, audited permissions enforced on every action.</p>
          </div>

          <div style="background: var(--bg-card); border: 1px solid var(--border); padding: 2rem; border-radius: 16px;">
            <div style="width: 40px; height: 40px; background: rgba(239, 68, 68, 0.1); border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-bottom: 1.5rem;">
              <i data-lucide="camera" style="color: var(--danger); width: 20px; height: 20px;"></i>
            </div>
            <h3 style="font-size: 1.1rem; margin-bottom: 0.75rem;">Field verification</h3>
            <p style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;">Officers capture before/after photos, log costs and materials, and close tickets with evidence — a complete audit trail from report to resolution.</p>
          </div>

        </div>
      </div>
    </section>

    <!-- NEW: METRICS BANNER -->
    <section class="section" style="background: #0B1121; color: white; border-top: none; border-bottom: none; padding: 4rem 1.5rem;">
      <div class="container" style="max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 2rem;">
        
        <div style="flex: 1; min-width: 200px;">
          <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 0.5rem; font-weight: 600;">Complaints resolved</div>
          <div style="font-size: 3rem; font-weight: 700; display: flex; align-items: baseline;"><span class="count-up" data-target="12400">0</span>+</div>
        </div>

        <div style="flex: 1; min-width: 200px;">
          <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 0.5rem; font-weight: 600;">SLA compliance rate</div>
          <div style="font-size: 3rem; font-weight: 700; display: flex; align-items: baseline;"><span class="count-up" data-target="96">0</span>%</div>
        </div>

        <div style="flex: 1; min-width: 200px;">
          <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 0.5rem; font-weight: 600;">Average citizen rating</div>
          <div style="font-size: 3rem; font-weight: 700; display: flex; align-items: baseline;"><span class="count-up" data-target="4.8" data-decimal="1">0</span>/5</div>
        </div>

        <div style="flex: 1; min-width: 200px;">
          <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 0.5rem; font-weight: 600;">Faster routing with AI</div>
          <div style="font-size: 3rem; font-weight: 700; display: flex; align-items: baseline;"><span class="count-up" data-target="3">0</span>x</div>
        </div>

      </div>
    </section>

    <!-- NEW: TESTIMONIALS -->
    <section class="section" style="background-color: var(--bg-primary);">
      <div class="container" style="max-width: 1200px; margin: 0 auto;">
        
        <div style="text-align: center; margin-bottom: 4rem;">
          <div style="font-size: 0.85rem; font-weight: 700; color: var(--success); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1rem;">Testimonials</div>
          <h2 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">Loved by citizens and city teams alike</h2>
          <p style="color: var(--text-secondary); font-size: 1.1rem; max-width: 600px; margin: 0 auto;">From the citizen filing a report to the supervisor clearing the queue — hear it from the people who use AI Smart Civic every day.</p>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
          
          <div style="background: var(--bg-card); border: 1px solid var(--border); padding: 2rem; border-radius: 16px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div style="display: flex; gap: 0.25rem; color: #f59e0b; margin-bottom: 1rem;">
                <i data-lucide="star" style="width: 16px; height: 16px; fill: #f59e0b;"></i><i data-lucide="star" style="width: 16px; height: 16px; fill: #f59e0b;"></i><i data-lucide="star" style="width: 16px; height: 16px; fill: #f59e0b;"></i><i data-lucide="star" style="width: 16px; height: 16px; fill: #f59e0b;"></i><i data-lucide="star" style="width: 16px; height: 16px; fill: #f59e0b;"></i>
              </div>
              <p style="color: var(--text-primary); font-size: 1.05rem; line-height: 1.6; margin-bottom: 2rem;">"We used to lose a day just sorting complaints into departments. Now the AI routes them before our morning stand-up. Resolution times have dropped by nearly half."</p>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
              <div style="width: 40px; height: 40px; border-radius: 50%; background: #10b981; color: white; display: flex; align-items: center; justify-content: center; font-weight: 700;">AK</div>
              <div>
                <div style="font-weight: 600; font-size: 0.95rem;">Ahmed Khan</div>
                <div style="font-size: 0.85rem; color: var(--text-muted);">Municipal Admin, Metropolitan City</div>
              </div>
            </div>
          </div>

          <div style="background: var(--bg-card); border: 1px solid var(--border); padding: 2rem; border-radius: 16px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div style="display: flex; gap: 0.25rem; color: #f59e0b; margin-bottom: 1rem;">
                <i data-lucide="star" style="width: 16px; height: 16px; fill: #f59e0b;"></i><i data-lucide="star" style="width: 16px; height: 16px; fill: #f59e0b;"></i><i data-lucide="star" style="width: 16px; height: 16px; fill: #f59e0b;"></i><i data-lucide="star" style="width: 16px; height: 16px; fill: #f59e0b;"></i><i data-lucide="star" style="width: 16px; height: 16px; fill: #f59e0b;"></i>
              </div>
              <p style="color: var(--text-primary); font-size: 1.05rem; line-height: 1.6; margin-bottom: 2rem;">"The SLA countdown changed how my team works. Nobody wants a ticket going red on the board. For the first time, leadership can see exactly where we are."</p>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
              <div style="width: 40px; height: 40px; border-radius: 50%; background: #3b82f6; color: white; display: flex; align-items: center; justify-content: center; font-weight: 700;">RM</div>
              <div>
                <div style="font-weight: 600; font-size: 0.95rem;">Supv. Khalid Mehmood</div>
                <div style="font-size: 0.85rem; color: var(--text-muted);">Supervisor, Water & Sanitation</div>
              </div>
            </div>
          </div>

          <div style="background: var(--bg-card); border: 1px solid var(--border); padding: 2rem; border-radius: 16px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div style="display: flex; gap: 0.25rem; color: #f59e0b; margin-bottom: 1rem;">
                <i data-lucide="star" style="width: 16px; height: 16px; fill: #f59e0b;"></i><i data-lucide="star" style="width: 16px; height: 16px; fill: #f59e0b;"></i><i data-lucide="star" style="width: 16px; height: 16px; fill: #f59e0b;"></i><i data-lucide="star" style="width: 16px; height: 16px; fill: #f59e0b;"></i><i data-lucide="star" style="width: 16px; height: 16px; fill: #f59e0b;"></i>
              </div>
              <p style="color: var(--text-primary); font-size: 1.05rem; line-height: 1.6; margin-bottom: 2rem;">"As a citizen I can report an issue at 11pm and see it accepted, classified, and assigned before I go to bed. That transparency builds real trust in local government."</p>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
              <div style="width: 40px; height: 40px; border-radius: 50%; background: #8b5cf6; color: white; display: flex; align-items: center; justify-content: center; font-weight: 700;">ZK</div>
              <div>
                <div style="font-weight: 600; font-size: 0.95rem;">Zoya Khan</div>
                <div style="font-size: 0.85rem; color: var(--text-muted);">Citizen, Ward 2</div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- NEW: FAQ -->
    <section class="section" style="background-color: var(--bg-card);">
      <div class="container" style="max-width: 800px; margin: 0 auto;">
        
        <div style="text-align: center; margin-bottom: 4rem;">
          <div style="font-size: 0.85rem; font-weight: 700; color: var(--success); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1rem;">FAQ</div>
          <h2 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">Frequently asked questions</h2>
          <p style="color: var(--text-secondary); font-size: 1.1rem; max-width: 600px; margin: 0 auto;">Everything you need to know about deploying AI Smart Civic in your community. Can't find your answer? Reach out to our team.</p>
        </div>

        <div class="faq-container">
          
          <div class="faq-item" style="border-bottom: 1px solid var(--border); padding: 1.5rem 0; cursor: pointer;">
            <div class="faq-question" style="display: flex; justify-content: space-between; align-items: center; font-weight: 600; font-size: 1.1rem; color: var(--text-primary);">
              How does the AI complaint classification actually work?
              <i data-lucide="chevron-down" class="faq-icon" style="transition: transform 0.3s; color: var(--text-muted);"></i>
            </div>
            <div class="faq-answer" style="display: none; padding-top: 1rem; color: var(--text-secondary); line-height: 1.6;">
              Our system uses a specialized Gemini AI model that processes both the text description and any uploaded photos. It extracts keywords, analyzes visual evidence (like a pothole or broken streetlight), and cross-references this with municipal department categories to automatically assign the ticket to the correct routing queue.
            </div>
          </div>

          <div class="faq-item" style="border-bottom: 1px solid var(--border); padding: 1.5rem 0; cursor: pointer;">
            <div class="faq-question" style="display: flex; justify-content: space-between; align-items: center; font-weight: 600; font-size: 1.1rem; color: var(--text-primary);">
              What happens if the AI misclassifies a complaint?
              <i data-lucide="chevron-down" class="faq-icon" style="transition: transform 0.3s; color: var(--text-muted);"></i>
            </div>
            <div class="faq-answer" style="display: none; padding-top: 1rem; color: var(--text-secondary); line-height: 1.6;">
              Supervisors and Admins have full override capabilities. If a ticket lands in the wrong department, it can be re-routed with a single click. The AI also logs these corrections and learns from them to improve future routing accuracy.
            </div>
          </div>

          <div class="faq-item" style="border-bottom: 1px solid var(--border); padding: 1.5rem 0; cursor: pointer;">
            <div class="faq-question" style="display: flex; justify-content: space-between; align-items: center; font-weight: 600; font-size: 1.1rem; color: var(--text-primary);">
              Is our municipal data secure?
              <i data-lucide="chevron-down" class="faq-icon" style="transition: transform 0.3s; color: var(--text-muted);"></i>
            </div>
            <div class="faq-answer" style="display: none; padding-top: 1rem; color: var(--text-secondary); line-height: 1.6;">
              Yes. We use industry-standard encryption for data at rest and in transit. Access is strictly controlled via Role-Based Access Control (RBAC), and all critical actions are recorded in an immutable audit log.
            </div>
          </div>

          <div class="faq-item" style="border-bottom: 1px solid var(--border); padding: 1.5rem 0; cursor: pointer;">
            <div class="faq-question" style="display: flex; justify-content: space-between; align-items: center; font-weight: 600; font-size: 1.1rem; color: var(--text-primary);">
              Can we migrate our existing complaint backlog?
              <i data-lucide="chevron-down" class="faq-icon" style="transition: transform 0.3s; color: var(--text-muted);"></i>
            </div>
            <div class="faq-answer" style="display: none; padding-top: 1rem; color: var(--text-secondary); line-height: 1.6;">
              Absolutely. We provide data migration tools and APIs that allow you to import historical tickets via CSV or JSON. The AI can even bulk-classify these older tickets to fit into the new departmental structure.
            </div>
          </div>

          <div class="faq-item" style="border-bottom: 1px solid var(--border); padding: 1.5rem 0; cursor: pointer;">
            <div class="faq-question" style="display: flex; justify-content: space-between; align-items: center; font-weight: 600; font-size: 1.1rem; color: var(--text-primary);">
              How long does deployment take?
              <i data-lucide="chevron-down" class="faq-icon" style="transition: transform 0.3s; color: var(--text-muted);"></i>
            </div>
            <div class="faq-answer" style="display: none; padding-top: 1rem; color: var(--text-secondary); line-height: 1.6;">
              Standard deployments take between 2 to 4 weeks. This includes setting up your custom organizational chart, configuring SLAs, importing data, and conducting initial training for supervisors.
            </div>
          </div>

          <div class="faq-item" style="border-bottom: 1px solid var(--border); padding: 1.5rem 0; cursor: pointer;">
            <div class="faq-question" style="display: flex; justify-content: space-between; align-items: center; font-weight: 600; font-size: 1.1rem; color: var(--text-primary);">
              Do you provide training for field officers and supervisors?
              <i data-lucide="chevron-down" class="faq-icon" style="transition: transform 0.3s; color: var(--text-muted);"></i>
            </div>
            <div class="faq-answer" style="display: none; padding-top: 1rem; color: var(--text-secondary); line-height: 1.6;">
              Yes, our onboarding packages include virtual and on-site training sessions (depending on your tier), comprehensive documentation, and a dedicated Customer Success Manager for the first 90 days.
            </div>
          </div>

          <div class="faq-item" style="border-bottom: 1px solid var(--border); padding: 1.5rem 0; cursor: pointer;">
            <div class="faq-question" style="display: flex; justify-content: space-between; align-items: center; font-weight: 600; font-size: 1.1rem; color: var(--text-primary);">
              Can citizens track their complaints without an account?
              <i data-lucide="chevron-down" class="faq-icon" style="transition: transform 0.3s; color: var(--text-muted);"></i>
            </div>
            <div class="faq-answer" style="display: none; padding-top: 1rem; color: var(--text-secondary); line-height: 1.6;">
              Yes! Citizens receive a unique tracking code (like a courier tracking number) when they submit a report. They can enter this code on the public portal to see real-time updates without needing to create or remember a password.
            </div>
          </div>
          
          <div class="faq-item" style="border-bottom: 1px solid var(--border); padding: 1.5rem 0; cursor: pointer;">
            <div class="faq-question" style="display: flex; justify-content: space-between; align-items: center; font-weight: 600; font-size: 1.1rem; color: var(--text-primary);">
              What happens when the AI API goes down?
              <i data-lucide="chevron-down" class="faq-icon" style="transition: transform 0.3s; color: var(--text-muted);"></i>
            </div>
            <div class="faq-answer" style="display: none; padding-top: 1rem; color: var(--text-secondary); line-height: 1.6;">
              We have a robust fallback mechanism. If the AI service is unreachable, the system automatically falls back to manual routing mode, ensuring that citizens can still submit complaints without interruption.
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- NEW: CTA BANNER -->
    <section class="section" style="background-color: var(--bg-primary); padding: 6rem 1.5rem;">
      <div class="container" style="max-width: 1000px; margin: 0 auto; background: var(--bg-card); border: 1px solid var(--border); border-radius: 24px; padding: 4rem 2rem; text-align: center; box-shadow: var(--shadow);">
        <h2 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">Ready to turn complaints into resolutions?</h2>
        <p style="color: var(--text-secondary); font-size: 1.1rem; margin-bottom: 2.5rem;">Join forward-thinking municipalities using AI to work smarter. Start for free in minutes — no credit card required.</p>
        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
          <a href="portal.html" class="btn btn-primary" style="padding: 0.75rem 2rem; font-size: 1.05rem;">Start free today <i data-lucide="arrow-right" style="width:18px;"></i></a>
          <a href="#" class="btn btn-outline" style="padding: 0.75rem 2rem; font-size: 1.05rem;"><i data-lucide="calendar" style="width:18px;"></i> Book a live demo</a>
        </div>
      </div>
    </section>
'''
    content = content[:insert_index] + html_to_inject + '\n' + content[insert_index:]
    print("Inserted grid, metrics, testimonials, FAQ.")

# 2. Replace Footer
footer_start = content.find('<!-- 8. PROFESSIONAL FOOTER -->')
footer_end_tag = '</footer>'
footer_end = content.find(footer_end_tag, footer_start)
if footer_start != -1 and footer_end != -1:
    new_footer = '''<!-- 8. PROFESSIONAL FOOTER (REPLACED) -->
    <footer style="background: var(--bg-card); border-top: 1px solid var(--border); padding: 5rem 1.5rem 2rem 1.5rem;">
      <div class="container" style="max-width: 1200px; margin: 0 auto;">
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 3rem; margin-bottom: 4rem;">
          
          <div style="grid-column: span 2;">
            <a href="index.html" class="logo" style="display:flex; align-items:flex-start; gap:0.5rem; text-decoration:none; margin-bottom: 1.5rem;">
              <i data-lucide="shield-check" style="width:20px; margin-top:2px;"></i>
              <div style="display:flex; flex-direction:column; align-items:flex-start; line-height:1;">
                  <span style="white-space:nowrap; font-size:1.1rem; font-weight:700;">AI Smart Civic</span>
              </div>
            </a>
            <p style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.5rem; max-width: 250px;">
              The AI-powered civic operations platform connecting citizens, municipal teams, and intelligent technology.
            </p>
            <div style="display: flex; gap: 1rem; color: var(--text-muted);">
              <i data-lucide="twitter" style="width: 20px; cursor: pointer; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-muted)'"></i>
              <i data-lucide="linkedin" style="width: 20px; cursor: pointer; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-muted)'"></i>
              <i data-lucide="github" style="width: 20px; cursor: pointer; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-muted)'"></i>
              <i data-lucide="mail" style="width: 20px; cursor: pointer; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-muted)'"></i>
            </div>
          </div>

          <div>
            <h4 style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1.5rem; color: var(--text-primary);">Product</h4>
            <div style="display: flex; flex-direction: column; gap: 1rem;">
              <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-secondary)'">Features</a>
              <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-secondary)'">Integrations</a>
              <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-secondary)'">Changelog</a>
              <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-secondary)'">Roadmap</a>
            </div>
          </div>

          <div>
            <h4 style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1.5rem; color: var(--text-primary);">Company</h4>
            <div style="display: flex; flex-direction: column; gap: 1rem;">
              <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-secondary)'">About</a>
              <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-secondary)'">Careers</a>
              <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-secondary)'">Blog</a>
              <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-secondary)'">Press kit</a>
              <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-secondary)'">Contact</a>
            </div>
          </div>

          <div>
            <h4 style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1.5rem; color: var(--text-primary);">Resources</h4>
            <div style="display: flex; flex-direction: column; gap: 1rem;">
              <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-secondary)'">Documentation</a>
              <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-secondary)'">API reference</a>
              <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-secondary)'">Security</a>
              <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-secondary)'">Status</a>
              <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-secondary)'">Community</a>
            </div>
          </div>

          <div>
            <h4 style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1.5rem; color: var(--text-primary);">Legal</h4>
            <div style="display: flex; flex-direction: column; gap: 1rem;">
              <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-secondary)'">Privacy Policy</a>
              <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-secondary)'">Terms of Service</a>
              <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-secondary)'">SLA Terms</a>
              <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s;" onmouseover="this.style.color='var(--brand-primary)'" onmouseout="this.style.color='var(--text-secondary)'">Data Processing</a>
            </div>
          </div>
          
        </div>

        <div style="border-top: 1px solid var(--border); padding-top: 2rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
          <div style="color: var(--text-muted); font-size: 0.85rem;">
            &copy; 2026 AI Smart Civic. All municipal data encrypted & logged.
          </div>
          <div style="color: var(--text-muted); font-size: 0.85rem;">
            Built for citizens, teams, and the communities they serve.
          </div>
        </div>
      </div>
    </footer>'''
    content = content[:footer_start] + new_footer + content[footer_end + len(footer_end_tag):]
    print("Inserted mega footer.")

# 3. Insert Scripts for Interactivity
script_inject = '''
    <!-- NEW: PAGE INTERACTIVITY SCRIPTS -->
    <script>
      document.addEventListener('DOMContentLoaded', () => {
        // FAQ Accordion
        const faqItems = document.querySelectorAll('.faq-item');
        faqItems.forEach(item => {
          item.addEventListener('click', () => {
            const answer = item.querySelector('.faq-answer');
            const icon = item.querySelector('.faq-icon');
            const isOpen = answer.style.display === 'block';
            
            // Close all other FAQs
            faqItems.forEach(otherItem => {
              otherItem.querySelector('.faq-answer').style.display = 'none';
              otherItem.querySelector('.faq-icon').style.transform = 'rotate(0deg)';
            });

            if (!isOpen) {
              answer.style.display = 'block';
              icon.style.transform = 'rotate(180deg)';
            }
          });
        });

        // Animated Counters
        const counters = document.querySelectorAll('.count-up');
        const observer = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              const el = entry.target;
              if (el.dataset.animated) return;
              el.dataset.animated = "true";
              
              const target = parseFloat(el.getAttribute('data-target'));
              const isDecimal = el.hasAttribute('data-decimal');
              const duration = 2000;
              const frameDuration = 1000 / 60;
              const totalFrames = Math.round(duration / frameDuration);
              let frame = 0;
              
              const counter = setInterval(() => {
                frame++;
                const progress = frame / totalFrames;
                // Easing out cubic
                const easeOut = 1 - Math.pow(1 - progress, 3);
                const currentVal = target * easeOut;
                
                if (isDecimal) {
                  el.innerText = currentVal.toFixed(1);
                } else {
                  el.innerText = Math.round(currentVal).toLocaleString();
                }
                
                if (frame === totalFrames) {
                  clearInterval(counter);
                  if (isDecimal) {
                    el.innerText = target.toFixed(1);
                  } else {
                    el.innerText = Math.round(target).toLocaleString();
                  }
                }
              }, frameDuration);
            }
          });
        }, { threshold: 0.5 });
        
        counters.forEach(counter => observer.observe(counter));
      });
    </script>
'''
body_end = content.rfind('</body>')
if body_end != -1:
    content = content[:body_end] + script_inject + '\n' + content[body_end:]
    print("Inserted JS.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Injection completed successfully!")
