    async def test_path_traversal_v2(self, ws) -> List[Dict]:
        """
        Enhanced path traversal testing
        """
        Logger.info("Testing path traversal with file disclosure detection...")
        
        results = []
        payloads = WSPayloads.get_path_traversal()[:50]
        
        base_message = self.sample_messages[0] if self.sample_messages else '{"filename": "test.txt"}'
        
        for payload in payloads:
            try:
                if self.learning_complete and self.message_intel.detected_format == MessageFormat.JSON:
                    injected_messages = self.message_intel.inject_payload_into_message(
                        base_message, payload
                    )
                else:
                    injected_messages = [json.dumps({"action": "read_file", "filename": payload})]
                
                for msg in injected_messages:
                    await ws.send(msg)
                    self.messages_sent += 1
                    
                    try:
                        response = await asyncio.wait_for(ws.recv(), timeout=2.0)
                        self.messages_received += 1
                        
                        # REAL VERIFICATION
                        is_vuln, confidence, description = self.verifier.verify_path_traversal(
                            response, payload
                        )
                        
                        if is_vuln and confidence != ConfidenceLevel.LOW:
                            Logger.vuln(f"Path Traversal [{confidence.value}]: {description}")
                            Logger.vuln(f"Payload: {payload[:80]}")
                            
                            self.vulnerabilities.append({
                                'type': 'Path Traversal',
                                'severity': confidence.value,
                                'confidence': confidence.value,
                                'description': description,
                                'payload': payload,
                                'response_snippet': response[:200],
                                'recommendation': 'Validate and sanitize all file paths'
                            })
                            results.append({'payload': payload, 'confidence': confidence.value})
                    
                    except asyncio.TimeoutError:
                        pass
                    
                    await asyncio.sleep(0.05)
            
            except Exception as e:
                continue
        
        return results
    
    async def test_xxe_v2(self, ws) -> List[Dict]:
        """
        Enhanced XXE testing
        """
        Logger.info("Testing XXE with entity detection...")
        
        results = []
        payloads = WSPayloads.get_xxe()[:30]
        
        for payload in payloads:
            try:
                # XXE payloads are XML, wrap in JSON message
                msg = json.dumps({"action": "parse_xml", "xml": payload})
                
                await ws.send(msg)
                self.messages_sent += 1
                
                try:
                    response = await asyncio.wait_for(ws.recv(), timeout=2.0)
                    self.messages_received += 1
                    
                    # Check for XXE indicators
                    xxe_indicators = ['<!entity', 'system', 'file://', 'root:', 'XML']
                    if any(ind.lower() in response.lower() for ind in xxe_indicators):
                        Logger.vuln(f"XXE [HIGH]: Entity processing detected")
                        Logger.vuln(f"Payload: {payload[:80]}")
                        
                        self.vulnerabilities.append({
                            'type': 'XML External Entity (XXE)',
                            'severity': 'HIGH',
                            'confidence': 'HIGH',
                            'description': 'XXE vulnerability detected - external entities processed',
                            'payload': payload,
                            'response_snippet': response[:200],
                            'recommendation': 'Disable external entity processing in XML parser'
                        })
                        results.append({'payload': payload, 'confidence': 'HIGH'})
                
                except asyncio.TimeoutError:
                    pass
                
                await asyncio.sleep(0.05)
            
            except Exception as e:
                continue
        
        return results
    
    async def test_nosql_injection_v2(self, ws) -> List[Dict]:
        """
        Enhanced NoSQL injection testing
        """
        Logger.info("Testing NoSQL injection with query manipulation...")
        
        results = []
        payloads = WSPayloads.get_nosql_injection()[:50]
        
        for payload in payloads:
            try:
                # NoSQL payloads often use special operators
                msg = json.dumps({"action": "find_user", "query": {"username": payload}})
                
                await ws.send(msg)
                self.messages_sent += 1
                
                try:
                    response = await asyncio.wait_for(ws.recv(), timeout=2.0)
                    self.messages_received += 1
                    
                    # Check for NoSQL indicators
                    nosql_indicators = ['mongodb', 'bson', 'query error', '$ne', '$gt']
                    if any(ind.lower() in response.lower() for ind in nosql_indicators):
                        Logger.vuln(f"NoSQL Injection [HIGH]: Query manipulation detected")
                        Logger.vuln(f"Payload: {payload[:80]}")
                        
                        self.vulnerabilities.append({
                            'type': 'NoSQL Injection',
                            'severity': 'HIGH',
                            'confidence': 'HIGH',
                            'description': 'NoSQL injection vulnerability detected',
                            'payload': payload,
                            'response_snippet': response[:200],
                            'recommendation': 'Use parameterized queries and input validation'
                        })
                        results.append({'payload': payload, 'confidence': 'HIGH'})
                
                except asyncio.TimeoutError:
                    pass
                
                await asyncio.sleep(0.05)
            
            except Exception as e:
                continue
        
        return results
