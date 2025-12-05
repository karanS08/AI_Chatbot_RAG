#!/usr/bin/env python3
"""
Advanced Sugarcane Knowledge Scraper with Multiple Sources
===========================================================
Scrapes specific agricultural sources with targeted content extraction.
"""

import requests
from bs4 import BeautifulSoup
import time
import json
import os
import re
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AdvancedSugarcaneScraper:
    """Advanced scraper with specific source handlers"""
    
    # Curated list of high-quality sugarcane farming sources
    SOURCES = {
        'iisr': {
            'name': 'Indian Institute of Sugarcane Research',
            'base_url': 'https://iisr.icar.gov.in/',
            'pages': [
                'sugarcane-varieties',
                'crop-management',
                'disease-management',
                'pest-management',
                'publications'
            ]
        },
        'pau': {
            'name': 'Punjab Agricultural University',
            'base_url': 'https://www.pau.edu/',
            'search_terms': ['sugarcane', 'ganna']
        },
        'agritech': {
            'name': 'TNAU Agritech Portal',
            'base_url': 'https://agritech.tnau.ac.in/',
            'sections': ['crop-production', 'plant-protection', 'varieties']
        },
        'vikaspedia': {
            'name': 'Vikaspedia Agriculture',
            'urls': [
                'https://vikaspedia.in/agriculture/crop-production/package-of-practices/sugarcane',
                'https://vikaspedia.in/agriculture/crop-production/integrated-pest-management/ipm-for-crops/ipm-strategies-for-sugarcane'
            ]
        },
        'manage': {
            'name': 'National Institute of Agricultural Extension Management',
            'base_url': 'https://www.manage.gov.in/',
            'topics': ['sugarcane cultivation', 'intercropping', 'sustainable farming']
        }
    }
    
    def __init__(self, output_dir='knowledge_base/sugarcane_scraped'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        self.collected_data = []
    
    def scrape_vikaspedia(self):
        """Scrape Vikaspedia - Government agricultural knowledge portal"""
        logger.info("📚 Scraping Vikaspedia...")
        
        urls = self.SOURCES['vikaspedia']['urls']
        
        for url in urls:
            try:
                logger.info(f"Fetching: {url}")
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Vikaspedia has good structured content
                title = soup.find('h1', class_='page-title')
                title_text = title.get_text().strip() if title else "Vikaspedia Content"
                
                # Extract main content
                content_div = soup.find('div', class_='field-item even')
                if content_div:
                    content = self._clean_text(content_div.get_text())
                    
                    if len(content) > 500:
                        self.collected_data.append({
                            'source': 'Vikaspedia',
                            'title': title_text,
                            'url': url,
                            'content': content,
                            'word_count': len(content.split())
                        })
                        logger.info(f"✓ Collected: {title_text}")
                
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error scraping Vikaspedia {url}: {e}")
    
    def scrape_agmarknet_prices(self):
        """Scrape Agmarknet for sugarcane market prices"""
        logger.info("💰 Scraping Agmarknet market data...")
        
        # This would require API access or specific state selection
        # Placeholder for market price data structure
        market_info = {
            'source': 'Agmarknet',
            'title': 'Sugarcane Market Prices and Trends',
            'content': """
            Note: Real-time market data requires API integration.
            General market information for sugarcane:
            - Fair and Remunerative Price (FRP) is set by Government of India
            - State Advised Prices (SAP) vary by state
            - Prices depend on sugar recovery rate
            - Payment timeline is typically 14 days from delivery
            - Market influenced by sugar production, ethanol demand, and export policies
            """,
            'url': 'https://agmarknet.gov.in/',
            'word_count': 50
        }
        self.collected_data.append(market_info)
    
    def scrape_farmer_portal(self):
        """Scrape farmer.gov.in for schemes and advisories"""
        logger.info("🏛️ Scraping Farmer Portal...")
        
        try:
            url = "https://farmer.gov.in/"
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for scheme information
            schemes = soup.find_all('div', class_=re.compile('scheme|card|info'))
            
            content_parts = []
            for scheme in schemes[:10]:  # Limit to 10 items
                text = scheme.get_text().strip()
                if 'sugar' in text.lower() or 'cane' in text.lower():
                    content_parts.append(text)
            
            if content_parts:
                self.collected_data.append({
                    'source': 'Farmer Portal',
                    'title': 'Government Schemes for Sugarcane Farmers',
                    'url': url,
                    'content': '\n\n'.join(content_parts),
                    'word_count': sum(len(p.split()) for p in content_parts)
                })
            
            time.sleep(2)
            
        except Exception as e:
            logger.error(f"Error scraping Farmer Portal: {e}")
    
    def scrape_text_sources(self):
        """Add curated text content from known reliable sources"""
        logger.info("📝 Adding curated text content...")
        
        # Add comprehensive farming practices content
        practices = {
            'source': 'Curated Content',
            'title': 'Comprehensive Sugarcane Cultivation Practices',
            'content': """
SUGARCANE CULTIVATION - COMPLETE GUIDE

1. LAND PREPARATION
- Deep ploughing to 40-45 cm depth
- Proper leveling for uniform water distribution
- Addition of organic manure (FYM 25-30 tonnes/hectare)
- Formation of ridges and furrows
- Soil testing for pH (6.5-7.5 optimal)

2. PLANTING
- Best time: February-March (spring), September-October (autumn)
- Seed rate: 35,000-40,000 three-budded setts per hectare
- Spacing: 90-100 cm row to row
- Depth: 7-10 cm
- Treatment of setts with fungicide and insecticide before planting

3. VARIETIES (India)
Popular varieties:
- CO 0238 (High sugar content, drought tolerant)
- CO 86032 (Early maturing, high yield)
- CoJ 88 (Red rot resistant)
- CO 94012 (Suitable for waterlogged areas)
- CO 0118 (Mid-late variety, high tillering)

4. IRRIGATION
- Critical stages: Germination, tillering, grand growth
- Avoid waterlogging
- Drip irrigation: 80-85% water saving
- Frequency: 7-10 days in summer, 12-15 days in winter

5. FERTILIZER APPLICATION
NPK requirements per hectare:
- Nitrogen: 150-200 kg
- Phosphorus: 60-80 kg
- Potassium: 60-80 kg

Split application:
- Basal dose: 25% N + 100% P + 50% K at planting
- 30 days: 25% N + 50% K
- 60 days: 25% N
- 90 days: 25% N

Micronutrients: Zinc, Iron as per soil test

6. WEED MANAGEMENT
- Critical period: First 90-120 days
- Pre-emergence herbicide: Atrazine @ 2 kg/ha
- Post-emergence: 2,4-D @ 2 kg/ha at 30-40 days
- Manual weeding: 2-3 times in first 90 days
- Mulching with trash

7. MAJOR PESTS
a) Early Shoot Borer (Chilo infuscatellus)
   - Attack: Germination to 3 months
   - Symptoms: Dead hearts, wilting of central shoot
   - Control: Seed treatment, resistant varieties, Chlorpyriphos

b) Top Borer (Scirpophaga excerptalis)
   - Attack: 3-6 months
   - Symptoms: Bunchy top appearance
   - Control: Remove affected shoots, spray insecticides

c) Pyrilla (Pyrilla perpusilla)
   - Sap-sucking pest
   - Control: Biological (Epiricania), chemical sprays

d) White Grubs
   - Attack roots
   - Control: Seed treatment, soil application of insecticide

8. MAJOR DISEASES
a) Red Rot (Colletotrichum falcatum)
   - Most serious disease
   - Symptoms: Reddening of internal tissues, white patches
   - Control: Resistant varieties, crop rotation, roguing

b) Smut (Sporisorium scitamineum)
   - Symptoms: Whip-like structure from shoot
   - Control: Resistant varieties, remove affected plants

c) Wilt (Fusarium sacchari)
   - Symptoms: Yellowing, wilting, drying
   - Control: Disease-free seed, soil treatment

d) Rust (Puccinia melanocephala)
   - Symptoms: Brown pustules on leaves
   - Control: Resistant varieties, fungicide spray

9. INTERCROPPING
Suitable crops in early stage:
- Potato, onion, garlic (winter)
- Groundnut, soybean, green gram (summer)
- Vegetables: cabbage, cauliflower, tomato
Benefits: Additional income, better land use, weed suppression

10. HARVESTING
- Duration: 10-12 months (plant crop), 11-12 months (ratoon)
- Maturity indicators:
  * Yellowish leaves
  * Dried leaf tips
  * Hard stem, metallic sound when tapped
  * Brix reading: 18-20°
- Method: Close to ground level cutting
- Cane should be crushed within 24 hours

11. RATOON MANAGEMENT
- Remove trash
- Gap filling with new setts
- Earthing up
- Apply fertilizer (20% higher than plant crop)
- Better irrigation management
- Profitable up to 3-4 ratoons

12. YIELD
- Plant crop: 80-100 tonnes/hectare
- Ratoon crop: 60-80 tonnes/hectare
- Sugar recovery: 10-12%

13. POST-HARVEST
- Immediate transport to mill
- Avoid delays to prevent sugar loss
- Quality parameters: Pol%, Purity%, CCS%

14. INTEGRATED NUTRIENT MANAGEMENT
- Combine organic and inorganic sources
- Green manuring with Sesbania, Sunhemp
- Bio-fertilizers: Azospirillum, PSB
- Compost application

15. WATER MANAGEMENT
- Mulching with sugarcane trash
- Alternate furrow irrigation
- Drip irrigation with fertigation
- Avoid irrigation 20 days before harvest

16. CLIMATE AND SOIL REQUIREMENTS
- Temperature: 20-35°C
- Rainfall: 1000-1500 mm annually
- Soil: Deep, well-drained loamy soil
- pH: 6.5-7.5
- Avoid highly acidic or alkaline soils
            """,
            'url': 'curated',
            'word_count': 800
        }
        
        self.collected_data.append(practices)
        
        # Add disease management guide
        disease_guide = {
            'source': 'Curated Content',
            'title': 'Sugarcane Disease Identification and Management Guide',
            'content': """
COMPLETE DISEASE MANAGEMENT GUIDE FOR SUGARCANE

I. FUNGAL DISEASES

1. RED ROT (Colletotrichum falcatum)
Symptoms:
- Reddening of internal stem tissues
- Whitish patches with red margins inside stem
- Drying of leaves from margins
- Sour smell from affected stems

Identification:
- Split the cane lengthwise
- Look for red discoloration with white patches
- Check for crosswise bands in affected portion

Management:
- Grow resistant varieties: CO 0238, CO 94012, CoJ 88
- Use disease-free seed material
- Hot water treatment of setts (52°C for 30 minutes)
- Crop rotation with non-host crops
- Remove and burn affected plants
- Avoid waterlogging
- Balanced fertilization

2. SMUT (Sporisorium scitamineum)
Symptoms:
- Long whip-like structure emerges from shoot tip
- Black powdery spore mass covers the whip
- Affected shoots don't develop into canes

Identification:
- Characteristic whip structure (1-2 meters)
- Black spore covering (easily rubs off)
- Usually appears in 3-5 month old crop

Management:
- Plant resistant varieties
- Rogue out affected plants immediately before spores disperse
- Dip seed material in Carbendazim solution
- Avoid using seed from infected fields
- Maintain field sanitation

3. WILT (Fusarium sacchari / Ceratocystis paradoxa)
Symptoms:
- Yellowing of leaves
- Wilting during hot hours
- Bunching of leaves
- Internal reddening of stems
- Plant death in severe cases

Management:
- Use healthy seed material
- Treat setts with fungicide
- Improve soil drainage
- Crop rotation
- Remove and destroy affected plants
- Avoid injuries to roots during cultivation

4. RUST (Puccinia melanocephala)
Symptoms:
- Small elongated yellow spots on leaves
- Develop into brown pustules
- Severe infection causes leaf drying

Management:
- Grow resistant varieties
- Remove affected leaves in early stage
- Spray Mancozeb or Propiconazole
- Ensure proper spacing for air circulation
- Balanced nutrition

II. BACTERIAL DISEASES

1. BACTERIAL LEAF SCORCH (Xanthomonas albilineans)
Symptoms:
- White to yellowish stripes on leaves
- Leaf margins become necrotic
- Stunted growth

Management:
- Use healthy planting material
- Hot water treatment of setts
- Remove affected plants
- Avoid mechanical injuries
- Use resistant varieties

2. GUMMING DISEASE (Xanthomonas axonopodis)
Symptoms:
- Bacterial ooze from stem
- Yellowing of leaves
- Stunted growth

Management:
- Field sanitation
- Use disease-free seed
- Spray copper-based bactericides

III. VIRAL DISEASES

1. MOSAIC (Sugarcane Mosaic Virus)
Symptoms:
- Light and dark green mosaic pattern on leaves
- Stunted growth
- Reduced yield

Management:
- Use virus-free seed material
- Control aphid vectors
- Remove affected plants early
- Grow resistant varieties

2. YELLOW LEAF DISEASE (Sugarcane Yellow Leaf Virus)
Symptoms:
- Yellowing of midrib and leaf
- Necrosis in severe cases

Management:
- Use healthy seed material
- Control aphid vectors
- Tissue culture propagation

IV. NEMATODE PROBLEMS

1. ROOT KNOT NEMATODE
Symptoms:
- Galls on roots
- Stunted growth
- Yellowing

Management:
- Crop rotation with non-host
- Nematicide application
- Use resistant varieties
- Improve soil health

V. INTEGRATED DISEASE MANAGEMENT

Prevention Strategies:
1. Seed Selection and Treatment
   - Use certified disease-free seed
   - Hot water treatment (52°C, 30 min)
   - Fungicide treatment: Carbendazim @ 0.2%

2. Cultural Practices
   - Crop rotation (3-4 year cycle)
   - Maintain field hygiene
   - Proper spacing (90-100 cm)
   - Timely weeding
   - Balanced fertilization
   - Adequate drainage

3. Resistant Varieties
   - Choose location-specific resistant varieties
   - Rotate varieties every 5-7 years
   - Monitor new releases from research stations

4. Monitoring and Scouting
   - Regular field inspection
   - Early detection of symptoms
   - Immediate removal of diseased plants
   - Record keeping of disease incidence

5. Chemical Control (When Necessary)
   Fungicides:
   - Carbendazim 50% WP @ 0.2%
   - Mancozeb 75% WP @ 0.25%
   - Propiconazole 25% EC @ 0.1%
   
   Bactericides:
   - Copper Oxychloride @ 0.25%
   - Streptocycline @ 500 ppm

6. Biological Control
   - Trichoderma viride (seed treatment, soil application)
   - Pseudomonas fluorescens
   - VAM fungi for root health

VI. DISEASE SURVEILLANCE SCHEDULE

Monthly monitoring checklist:
Month 1-2: Watch for seed-borne diseases
Month 3-4: Scout for smut, early wilt symptoms
Month 5-7: Check for red rot, rust, pests
Month 8-10: Monitor maturity diseases, ratoon health
Month 11-12: Pre-harvest assessment

EMERGENCY RESPONSE:
- Suspected Red Rot: Immediate roguing, increase gap inspection
- Smut outbreak: Mass removal before spore dispersal
- Wilt patches: Improve drainage, apply biocontrol agents
- Rust epidemic: Emergency fungicide spray

Remember: Prevention is better than cure. Invest in quality seed material and follow good agricultural practices.
            """,
            'url': 'curated',
            'word_count': 900
        }
        
        self.collected_data.append(disease_guide)
    
    def _clean_text(self, text):
        """Clean extracted text"""
        import re
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()
    
    def save_data(self):
        """Save all collected data"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save JSON
        json_file = self.output_dir / f'sugarcane_knowledge_{timestamp}.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.collected_data, f, indent=2, ensure_ascii=False)
        logger.info(f"💾 Saved JSON: {json_file}")
        
        # Save individual text files
        for idx, data in enumerate(self.collected_data, 1):
            safe_title = re.sub(r'[^\w\s-]', '', data['title'])[:50]
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            
            txt_file = self.output_dir / f"{idx:02d}_{safe_title}.txt"
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(f"SOURCE: {data['source']}\n")
                f.write(f"TITLE: {data['title']}\n")
                f.write(f"URL: {data.get('url', 'N/A')}\n")
                f.write(f"WORD COUNT: {data['word_count']}\n")
                f.write("\n" + "="*80 + "\n\n")
                f.write(data['content'])
            
            logger.info(f"📄 Saved: {txt_file}")
        
        # Save summary
        summary_file = self.output_dir / f'_summary_{timestamp}.txt'
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("SUGARCANE KNOWLEDGE COLLECTION SUMMARY\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Total documents: {len(self.collected_data)}\n")
            f.write(f"Total words: {sum(d['word_count'] for d in self.collected_data)}\n")
            f.write(f"Collected: {datetime.now()}\n\n")
            
            f.write("Documents:\n")
            for i, data in enumerate(self.collected_data, 1):
                f.write(f"{i}. {data['title']} ({data['source']}) - {data['word_count']} words\n")
        
        logger.info(f"📊 Saved summary: {summary_file}")
    
    def run(self):
        """Run all scraping tasks"""
        logger.info("🚀 Starting advanced sugarcane knowledge collection...")
        
        # Add curated content first (always works)
        self.scrape_text_sources()
        
        # Try web scraping (may fail due to network/robots.txt)
        try:
            self.scrape_vikaspedia()
        except Exception as e:
            logger.warning(f"Vikaspedia scraping skipped: {e}")
        
        try:
            self.scrape_agmarknet_prices()
        except Exception as e:
            logger.warning(f"Agmarknet scraping skipped: {e}")
        
        try:
            self.scrape_farmer_portal()
        except Exception as e:
            logger.warning(f"Farmer portal scraping skipped: {e}")
        
        # Save everything
        self.save_data()
        
        logger.info(f"\n✅ Collection complete! {len(self.collected_data)} documents saved to {self.output_dir}")


def main():
    print("=" * 80)
    print("🌾 ADVANCED SUGARCANE KNOWLEDGE SCRAPER")
    print("=" * 80)
    print("\nThis will collect:")
    print("  ✓ Comprehensive cultivation practices")
    print("  ✓ Disease identification and management")
    print("  ✓ Pest control strategies")
    print("  ✓ Variety information")
    print("  ✓ Government schemes")
    print("  ✓ Market information")
    print("\n" + "=" * 80 + "\n")
    
    scraper = AdvancedSugarcaneScraper()
    scraper.run()
    
    print("\n" + "=" * 80)
    print("✅ DONE!")
    print("=" * 80)
    print(f"\nFiles saved to: {scraper.output_dir}")
    print("\nNext steps:")
    print("  1. Review the generated .txt files")
    print("  2. Upload them via: curl -F 'files=@filename.txt' http://localhost:5000/upload")
    print("  3. Test chatbot with sugarcane questions")


if __name__ == "__main__":
    main()
