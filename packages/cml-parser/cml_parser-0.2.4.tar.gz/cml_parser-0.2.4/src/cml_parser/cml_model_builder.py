from typing import List, Optional, Any
from antlr4 import *
from .antlr.CMLParser import CMLParser
from .antlr.CMLVisitor import CMLVisitor
from .cml_objects import (
    CML,
    Domain,
    Subdomain,
    SubdomainType,
    ContextMap,
    Context,
    Relationship,
    RelationshipType,
    UseCase,
    Entity,
    ValueObject,
    DomainEvent,
    Enum,
    Aggregate,
    Service,
    Repository,
    Attribute,
    Operation,
    Attribute,
    Operation,
    Parameter,
    UserStory,
    Stakeholder,
    StakeholderGroup,
    ValueRegister,
    ValueCluster,
    Value,
    Application,
    Flow,
    FlowStep,
    Command,
    Coordination,
    CommandEvent,
    DataTransferObject,
    Module
)

class CMLModelBuilder(CMLVisitor):
    def __init__(self, filename: str = None):
        self.filename = filename
        self.cml = CML()
        self.context_map_obj_map = {} # Name -> Context
        self.subdomain_map = {} # Name -> Subdomain
        
        # Deferred linking
        self.deferred_context_map_links = [] # (ContextMap, [names])
        self.deferred_context_links = [] # (Context, [implements_names])
        
        self.current_domain = None
        self.current_subdomain = None
        self.current_context = None
        self.current_aggregate = None
        self.current_entity = None
        self.current_value_object = None
        self.current_domain_event = None
        self.current_module = None
        self.current_application = None
        self.current_stakeholder_group = None
        self.current_value_register = None
        self.current_value_cluster = None

    def visitDefinitions(self, ctx: CMLParser.DefinitionsContext):
        self.visitChildren(ctx)
        
        # Post-processing: Link contexts and subdomains
        self._link_references()
        
        return self.cml

    def _link_references(self):
        # Link ContextMap contains
        for cm, ctx_names in self.deferred_context_map_links:
            for name in ctx_names:
                ctx = self.context_map_obj_map.get(name)
                if ctx:
                    if ctx not in cm.contexts:
                        cm.contexts.append(ctx)
                    ctx.context_map = cm
        
        # Link BoundedContext implements
        for ctx, subdomain_names in self.deferred_context_links:
            for name in subdomain_names:
                sd = self.subdomain_map.get(name)
                if sd:
                    ctx.implements.append(sd)
                    sd.implementations.append(ctx)

    def visitContextMap(self, ctx: CMLParser.ContextMapContext):
        name = ctx.name().getText() if ctx.name() else "ContextMap"
        cm = ContextMap(name=name, type="SYSTEM_LANDSCAPE", state="AS_IS")
        
        # Process settings
        contains_list = []
        for setting in ctx.contextMapSetting():
            if setting.contextMapType():
                cm.type = setting.contextMapType().getText()
            elif setting.contextMapState():
                cm.state = setting.contextMapState().getText()
            elif setting.idList():
                # contains
                names = [id_node.getText() for id_node in setting.idList().name()]
                contains_list.extend(names)
            else:  # pragma: no cover
                pass
                
        if contains_list:
            self.deferred_context_map_links.append((cm, contains_list))
        
        # Process relationships
        for rel_ctx in ctx.relationship():
            rel = self.visitRelationship(rel_ctx)
            if rel:  # pragma: no branch
                cm.relationships.append(rel)
                # Add contexts to map if not present
                if rel.left and rel.left not in cm.contexts:
                    cm.contexts.append(rel.left)
                if rel.right and rel.right not in cm.contexts:
                    cm.contexts.append(rel.right)
        
        self.cml.context_maps.append(cm)
        return cm

    def visitRelationship(self, ctx: CMLParser.RelationshipContext):
        left_endpoint = ctx.relationshipEndpoint(0)
        right_endpoint = ctx.relationshipEndpoint(1)
        
        left_name = left_endpoint.name().getText()
        right_name = right_endpoint.name().getText()
        
        left_ctx = self._get_or_create_context(left_name)
        right_ctx = self._get_or_create_context(right_name)
        
        connection = ctx.relationshipConnection()
        rel_type = "Unknown"
        if connection.relationshipArrow():
            rel_type = connection.relationshipArrow().getText()
        elif connection.relationshipKeyword():
            rel_type = connection.relationshipKeyword().getText()
            
        # Extract roles
        roles = []
        for endpoint in [left_endpoint, right_endpoint]:
            if endpoint.relationshipRoles():
                for roles_ctx in endpoint.relationshipRoles():
                    for role in roles_ctx.relationshipRole():
                        roles.append(role.getText())
        
        rel = Relationship(left=left_ctx, right=right_ctx, type=rel_type, roles=roles)
        
        # Extract attributes
        if ctx.relationshipAttribute():
            for attr in ctx.relationshipAttribute():
                if 'implementationTechnology' in attr.getText():
                    rel.implementation_technology = attr.STRING().getText().strip('"')
                elif 'downstreamRights' in attr.getText():
                    if attr.downstreamRights():  # pragma: no branch
                        rel.downstream_rights = attr.downstreamRights().getText()
                elif 'exposedAggregates' in attr.getText():
                    if attr.idList():  # pragma: no branch
                        rel.exposed_aggregates = [n.getText() for n in attr.idList().name()]
                        
        return rel

    def _get_or_create_context(self, name: str) -> Context:
        if name in self.context_map_obj_map:
            return self.context_map_obj_map[name]
        
        ctx = Context(name=name)
        self.context_map_obj_map[name] = ctx
        if ctx not in self.cml.contexts:  # pragma: no branch
            self.cml.contexts.append(ctx)
        return ctx

    def visitBoundedContext(self, ctx: CMLParser.BoundedContextContext):
        name = ctx.name().getText()
        context = self._get_or_create_context(name)
        
        # Check implements/realizes
        implements_list = []
        
        for i in range(ctx.getChildCount()):
            child = ctx.getChild(i)
            if child.getText() == 'implements':
                # Next child should be idList
                next_child = ctx.getChild(i+1)
                if isinstance(next_child, CMLParser.IdListContext):  # pragma: no branch
                    names = [n.getText() for n in next_child.name()]
                    implements_list.extend(names)
        
        if implements_list:
            self.deferred_context_links.append((context, implements_list))
        
        self.current_context = context
        if ctx.body:
            self.visit(ctx.body)
        self.current_context = None
        
        return context

    def visitDomain(self, ctx: CMLParser.DomainContext):
        name = ctx.name().getText()
        domain = Domain(name=name, vision="")
        self.current_domain = domain
        
        if ctx.body:
            self.visit(ctx.body)
            
        self.cml.domains.append(domain)
        self.current_domain = None
        return domain

    def visitSubdomain(self, ctx: CMLParser.SubdomainContext):
        name = ctx.name().getText()
        sd_type = SubdomainType.GENERIC
        if ctx.subdomainType():
            type_str = ctx.subdomainType().getText()
            try:
                sd_type = SubdomainType(type_str)
            except ValueError:  # pragma: no cover (grammar restricts values)
                pass
                
        subdomain = Subdomain(name=name, type=sd_type, vision="", domain=self.current_domain)
        self.subdomain_map[name] = subdomain
        
        if self.current_domain:
            self.current_domain.subdomains.append(subdomain)
        else:  # pragma: no cover
            # Orphan subdomain, logic TBD
            pass
            
        prev_subdomain = getattr(self, 'current_subdomain', None)
        self.current_subdomain = subdomain
        
        if ctx.body:
            self.visit(ctx.body)
            
        self.current_subdomain = prev_subdomain
        return subdomain

    def visitAggregate(self, ctx: CMLParser.AggregateContext):
        name = ctx.name().getText()
        agg = Aggregate(name=name)
        
        if self.current_module:
            self.current_module.aggregates.append(agg)
            if self.current_context:
                agg.context = self.current_context
        elif self.current_context:
            agg.context = self.current_context
            self.current_context.aggregates.append(agg)
            
        self.current_aggregate = agg
        if ctx.body:
            self.visit(ctx.body)
        self.current_aggregate = None
        return agg

    def visitEntity(self, ctx: CMLParser.EntityContext):
        name = ctx.name(0).getText()
        entity = Entity(name=name)
        
        # Check extends
        if len(ctx.name()) > 1:
            entity.extends = ctx.name(1).getText()
        
        if ctx.entityBody():
            if 'aggregateRoot' in ctx.entityBody().getText(): 
                 entity.is_aggregate_root = True
            
            self.current_entity = entity
            for feature in ctx.entityBody().feature():
                self.visit(feature)
            self.current_entity = None
            
        if self.current_aggregate:
            entity.aggregate = self.current_aggregate
            self.current_aggregate.entities.append(entity)
        elif hasattr(self, 'current_subdomain') and self.current_subdomain:
            self.current_subdomain.entities.append(entity)
        elif hasattr(self, 'current_module') and self.current_module:
            self.current_module.domain_objects.append(entity)
            
        return entity

    def visitValueObject(self, ctx: CMLParser.ValueObjectContext):
        name = ctx.name(0).getText()
        vo = ValueObject(name=name)
        
        if len(ctx.name()) > 1:
            vo.extends = ctx.name(1).getText()
        
        if ctx.valueObjectBody():
            self.current_value_object = vo
            for feature in ctx.valueObjectBody().feature():
                self.visit(feature)
            self.current_value_object = None
            
        if self.current_aggregate:
            self.current_aggregate.value_objects.append(vo)
        elif hasattr(self, 'current_module') and self.current_module:
            self.current_module.domain_objects.append(vo)
        return vo

    def visitDomainEvent(self, ctx: CMLParser.DomainEventContext):
        name = ctx.name(0).getText()
        de = DomainEvent(name=name)
        
        if len(ctx.name()) > 1:
            de.extends = ctx.name(1).getText()
        
        if ctx.domainEventBody():
            if 'aggregateRoot' in ctx.domainEventBody().getText():
                de.is_aggregate_root = True
            if 'persistent' in ctx.domainEventBody().getText():
                de.persistent = True
                
            self.current_domain_event = de
            for feature in ctx.domainEventBody().feature():
                self.visit(feature)
            self.current_domain_event = None
            
        if self.current_aggregate:
            self.current_aggregate.domain_events.append(de)
        elif hasattr(self, 'current_module') and self.current_module:
            self.current_module.domain_objects.append(de)
        return de

    def visitEnumDecl(self, ctx: CMLParser.EnumDeclContext):
        name = ctx.name().getText()
        enum = Enum(name=name)
        
        if 'aggregateLifecycle' in ctx.getText():
            enum.is_aggregate_lifecycle = True
            
        if ctx.idList():
            enum.values = [id_node.getText() for id_node in ctx.idList().name()]
            
        if self.current_aggregate:
            self.current_aggregate.enums.append(enum)
        elif hasattr(self, 'current_module') and self.current_module:
            self.current_module.domain_objects.append(enum)
        return enum

    def visitAttribute(self, ctx: CMLParser.AttributeContext):
        name = ctx.name().getText()
        type_name = ctx.type_().getText()
        
        attr = Attribute(name=name, type=type_name)
        
        if ctx.reference:
            attr.is_reference = True
        if ctx.visibility():
            attr.visibility = ctx.visibility().getText()
        
        for child in ctx.getChildren():
            if child.getText() == 'key':
                attr.is_key = True
                break
        
        if hasattr(self, 'current_entity') and self.current_entity:
            self.current_entity.attributes.append(attr)
        elif hasattr(self, 'current_value_object') and self.current_value_object:
            self.current_value_object.attributes.append(attr)
        elif hasattr(self, 'current_domain_event') and self.current_domain_event:
            self.current_domain_event.attributes.append(attr)
            
        return attr

    def visitOperation(self, ctx: CMLParser.OperationContext):
        name = ctx.name().getText()
        op = Operation(name=name)
        
        if ctx.type_():
            op.return_type = ctx.type_().getText()
            
        if ctx.visibility():
            op.visibility = ctx.visibility().getText()
            
        if ctx.parameterList():
            for param_ctx in ctx.parameterList().parameter():
                p_name = param_ctx.name().getText()
                p_type = param_ctx.type_().getText()
                is_ref = '@' in param_ctx.getText()
                op.parameters.append(Parameter(name=p_name, type=p_type, is_reference=is_ref))
                
        if ctx.idList():
            op.throws = [t.getText() for t in ctx.idList().name()]

        # Heuristic: declarations without params/throws/hints are usually attributes, not operations
        if (
            not ctx.operationHint()
            and not ctx.idList()
            and not ctx.parameterList()
            and "(" not in ctx.getText()
        ):  # pragma: no cover
            attr_type = op.return_type or ""
            is_ref = False
            if attr_type.startswith("@"):
                attr_type = attr_type.lstrip("@")
                is_ref = True

            attr = Attribute(
                name=name,
                type=attr_type,
                is_reference=is_ref,
                visibility=op.visibility,
            )

            target = None
            if hasattr(self, 'current_entity') and self.current_entity:
                target = self.current_entity
            elif hasattr(self, 'current_value_object') and self.current_value_object:
                target = self.current_value_object
            elif hasattr(self, 'current_domain_event') and self.current_domain_event:
                target = self.current_domain_event

            if target:
                target.attributes.append(attr)
                return attr
            
        if hasattr(self, 'current_entity') and self.current_entity:
            self.current_entity.operations.append(op)
        elif hasattr(self, 'current_value_object') and self.current_value_object:
            self.current_value_object.operations.append(op)
        elif hasattr(self, 'current_domain_event') and self.current_domain_event:
            self.current_domain_event.operations.append(op)
        elif hasattr(self, 'current_service') and self.current_service:
            self.current_service.operations.append(op)
        elif hasattr(self, 'current_repository') and self.current_repository:  # pragma: no cover
            self.current_repository.operations.append(op)
            
        return op

    def visitService(self, ctx: CMLParser.ServiceContext):
        name = ctx.name().getText()
        svc = Service(name=name)
        
        self.current_service = svc
        if ctx.serviceBody:
            self.visit(ctx.serviceBody)
        self.current_service = None
        
        if self.current_aggregate:
            svc.aggregate = self.current_aggregate
            self.current_aggregate.services.append(svc)
        elif self.current_module:
            self.current_module.services.append(svc)
        elif self.current_context:
            self.current_context.services.append(svc)
            
        return svc

    def visitRepository(self, ctx: CMLParser.RepositoryContext):
        name = ctx.name().getText()
        repo = Repository(name=name)
        
        self.current_repository = repo
        if ctx.repositoryBody():
            for method in ctx.repositoryBody().repositoryMethod():
                self.visitRepositoryMethod(method)
        self.current_repository = None
        
        if self.current_aggregate:
            self.current_aggregate.repositories.append(repo)
            
        return repo

    def visitOwnerDecl(self, ctx: CMLParser.OwnerDeclContext):
        owner = ctx.name().getText()
        if self.current_aggregate:
            self.current_aggregate.owner = owner
        return owner

    def visitBoundedContextAttribute(self, ctx: CMLParser.BoundedContextAttributeContext):
        # Handle attributes like responsibilities, knowledgeLevel, etc.
        # These can apply to Context, Subdomain, or Aggregate
        
        target = None
        if self.current_aggregate:
            target = self.current_aggregate
        elif self.current_context:
            target = self.current_context
        elif self.current_subdomain:
            target = self.current_subdomain
        elif self.current_domain:
            target = self.current_domain
            
        if not target:  # pragma: no cover
            return
            
        if ctx.boundedContextType():
            if hasattr(target, 'type'):
                target.type = ctx.boundedContextType().getText()
                
        elif ctx.knowledgeLevel():
            if hasattr(target, 'knowledge_level'):
                target.knowledge_level = ctx.knowledgeLevel().getText()
                
        # Check for strings (responsibilities, vision, etc.)
        # Grammar: 'responsibilities' '=' STRING | 'domainVisionStatement' '=' STRING | ...
        
        text = ctx.getText()
        if 'responsibilities' in text:
            # Extract string. The string token is available in ctx.STRING()
            # But there might be multiple strings? No, rule has alternatives.
            if ctx.STRING():  # pragma: no branch
                # Remove quotes
                s = ctx.STRING().getText().strip('"')
                if hasattr(target, 'responsibilities'):
                    target.responsibilities = s
                    
        elif 'domainVisionStatement' in text:
            if ctx.STRING():  # pragma: no branch
                s = ctx.STRING().getText().strip('"')
                if hasattr(target, 'vision'):
                    target.vision = s
                    
        elif 'implementationTechnology' in text:
            if ctx.STRING():  # pragma: no branch
                s = ctx.STRING().getText().strip('"')
                if hasattr(target, 'implementation_technology'):
                    target.implementation_technology = s

    def visitSubdomainAttribute(self, ctx: CMLParser.SubdomainAttributeContext):
        if not self.current_subdomain:
            return
            
        if ctx.subdomainType():
            type_str = ctx.subdomainType().getText()
            try:
                self.current_subdomain.type = SubdomainType(type_str)
            except ValueError:  # pragma: no cover
                pass
                
        elif ctx.STRING():  # pragma: no cover
            # domainVisionStatement
            s = ctx.STRING().getText().strip('"')
            self.current_subdomain.vision = s

    def visitSetting(self, ctx: CMLParser.SettingContext):
        # basePackage currently ignored in the object model
        pass

    def visitRepositoryMethod(self, ctx: CMLParser.RepositoryMethodContext):
        name_ctx = ctx.name()
        name = name_ctx.getText() if name_ctx else None
        op = Operation(name=name)
        
        if ctx.type_():
            op.return_type = ctx.type_().getText()
            
        if ctx.visibility():
            op.visibility = ctx.visibility().getText()
            
        if ctx.parameterList():
            for param_ctx in ctx.parameterList().parameter():
                p_name = param_ctx.name().getText()
                p_type = param_ctx.type_().getText()
                is_ref = '@' in param_ctx.getText()
                op.parameters.append(Parameter(name=p_name, type=p_type, is_reference=is_ref))
                
        if ctx.idList():
            op.throws = [t.getText() for t in ctx.idList().name()]
            
        if self.current_repository:
            self.current_repository.operations.append(op)
        else:  # pragma: no cover
            pass
            
        return op

    def visitUseCase(self, ctx: CMLParser.UseCaseContext):
        name = ctx.name().getText()
        uc = UseCase(name=name)
        
        for element in ctx.useCaseBody():
            if element.useCaseActor():
                uc.actor = element.useCaseActor().STRING().getText().strip('"')
            elif element.useCaseBenefit():
                uc.benefit = element.useCaseBenefit().STRING().getText().strip('"')
            elif element.useCaseScope():
                uc.scope = element.useCaseScope().STRING().getText().strip('"')
            elif element.useCaseLevel():
                uc.level = element.useCaseLevel().STRING().getText().strip('"')
            elif element.useCaseInteractionsBlock():
                # Handle interactions block
                for item in element.useCaseInteractionsBlock().useCaseInteractionItem():
                    if item.useCaseReadOperation():
                        # Parse read operation - just store as string for now
                        read_op = item.useCaseReadOperation().getText()
                        uc.interactions.append(read_op)
                    elif item.STRING():
                        uc.interactions.append(item.STRING().getText().strip('"'))
                    elif item.useCaseInteractionId():
                        uc.interactions.append(item.useCaseInteractionId().getText())
                        
        self.cml.use_cases.append(uc)
        return uc

    def visitUserStory(self, ctx: CMLParser.UserStoryContext):
        name = ctx.name().getText()
        us = UserStory(name=name)
        
        bodies = ctx.userStoryBody()
        if bodies:
            body = bodies[0]
            
            # 'As' 'a' STRING
            # 'I' 'want' 'to' (ID | 'do')? STRING
            # 'so' 'that' STRING
            
            strings = body.STRING()
            if len(strings) >= 1:
                us.role = strings[0].getText().strip('"')
            if len(strings) >= 2:
                us.feature = strings[1].getText().strip('"')
            if len(strings) >= 3:
                us.benefit = strings[2].getText().strip('"')
                
        self.cml.user_stories.append(us)
        return us

    def visitStakeholderSection(self, ctx: CMLParser.StakeholderSectionContext):
        # 'Stakeholders' 'of' name '{' stakeholderItem* '}'
        # We ignore the 'of name' part for now as it's usually the project name
        if ctx.stakeholderItem():
            for item in ctx.stakeholderItem():
                self.visit(item)

    def visitStakeholderGroup(self, ctx: CMLParser.StakeholderGroupContext):
        name = ctx.name().getText()
        group = StakeholderGroup(name=name)
        
        self.current_stakeholder_group = group
        if ctx.stakeholder():
            for s in ctx.stakeholder():
                self.visit(s)
        self.current_stakeholder_group = None
        
        self.cml.stakeholder_groups.append(group)
        return group

    def visitStakeholder(self, ctx: CMLParser.StakeholderContext):
        name = ctx.name().getText()
        stakeholder = Stakeholder(name=name)
        
        if ctx.stakeholderAttribute():
            for attr in ctx.stakeholderAttribute():
                text = attr.getText()
                if 'influence' in text:
                    stakeholder.influence = attr.name().getText()
                elif 'interest' in text:
                    stakeholder.interest = attr.name().getText()
                elif 'priority' in text:
                    stakeholder.priority = attr.name().getText()
                elif 'impact' in text:
                    stakeholder.impact = attr.name().getText()
                elif attr.consequences():
                    for item in attr.consequences().consequenceItem():
                        stakeholder.consequences.append(item.getText())
                elif attr.consequenceItem():
                    stakeholder.consequences.append(attr.consequenceItem().getText())

        if self.current_stakeholder_group:
            self.current_stakeholder_group.stakeholders.append(stakeholder)
        elif self.current_value_cluster:
             # Value stakeholders are just references usually, but grammar allows full definition
             # We'll just add them to the main list if they are full definitions
             pass
        else:
            self.cml.stakeholders.append(stakeholder)
            
        return stakeholder

    def visitValueRegister(self, ctx: CMLParser.ValueRegisterContext):
        name = ctx.name(0).getText()
        register = ValueRegister(name=name)
        
        if len(ctx.name()) > 1:
            register.context = ctx.name(1).getText()
            
        self.current_value_register = register
        
        for cluster in ctx.valueCluster():
            self.visit(cluster)
            
        for value in ctx.value():
            self.visit(value)
            
        self.current_value_register = None
        self.cml.value_registers.append(register)
        return register

    def visitValueCluster(self, ctx: CMLParser.ValueClusterContext):
        name = ctx.name().getText()
        cluster = ValueCluster(name=name)
        
        if ctx.valueClusterAttribute():
            for attr in ctx.valueClusterAttribute():
                if 'core' in attr.getText():
                    cluster.core_value = attr.name().getText()
                elif 'demonstrator' in attr.getText():
                    cluster.demonstrator = attr.STRING().getText().strip('"')
                    
        self.current_value_cluster = cluster
        for value in ctx.value():
            self.visit(value)
        self.current_value_cluster = None
        
        if self.current_value_register:
            self.current_value_register.clusters.append(cluster)
            
        return cluster

    def visitValue(self, ctx: CMLParser.ValueContext):
        name = ctx.name().getText()
        value = Value(name=name)
        
        if ctx.valueAttribute():
            for attr in ctx.valueAttribute():
                if 'core' in attr.getText() or 'isCore' in attr.getText():
                    value.is_core = True
                elif 'demonstrator' in attr.getText():
                    value.demonstrator = attr.STRING().getText().strip('"')
                    
        if ctx.valueStakeholder():
            # These are usually just references to stakeholders
            for vs in ctx.valueStakeholder():
                s_name = vs.name().getText()
                # Create a placeholder stakeholder or look it up?
                # For now, just create a simple one
                value.stakeholders.append(Stakeholder(name=s_name))

        if self.current_value_cluster:
            self.current_value_cluster.values.append(value)
        elif self.current_value_register:
            self.current_value_register.values.append(value)
            
        return value

    def visitApplication(self, ctx: CMLParser.ApplicationContext):
        app = Application()
        self.current_application = app
        
        for element in ctx.applicationElement():
            if element.commandDecl():
                cmd_name = element.commandDecl().name().getText()
                app.commands.append(Command(name=cmd_name))
            elif element.flow():
                self.visit(element.flow())
            elif element.service():
                self.visit(element.service())
            elif element.coordination():
                self.visit(element.coordination())
                
        if self.current_module:
            self.current_module.application = app
        elif self.current_context:
            self.current_context.application = app
        else:
            pass
            
        self.current_application = None
        return app

    def visitFlow(self, ctx: CMLParser.FlowContext):
        name = ctx.name().getText()
        flow = Flow(name=name)
        
        for step in ctx.flowStep():
            flow_step = None
            if step.flowCommandStep():
                s = step.flowCommandStep()
                s_name = s.name().getText()
                flow_step = FlowStep(type="command", name=s_name)
                if s.flowCommandTail():
                    tail = s.flowCommandTail()
                    if tail.flowDelegate():
                        flow_step.delegate = tail.flowDelegate().name().getText()
                    if tail.flowEmitsClause():
                        # emits event A + B
                        if tail.flowEmitsClause().flowEventList():
                             flow_step.emits = [n.getText() for n in tail.flowEmitsClause().flowEventList().name()]
                             
            elif step.flowEventStep():
                s = step.flowEventStep()
                # event A + B triggers ...
                triggers = [n.getText() for n in s.flowEventTriggerList().name()]
                # ... triggers op1 + op2
                # flowInvocationList
                invocations = []
                inv_list = s.flowInvocationList()
                invocations.append(inv_list.flowInvocation().name().getText())
                for conn in inv_list.flowInvocationConnector():
                    invocations.append(conn.flowInvocation().name().getText())
                
                # We'll just store the first invocation as the name for now, or create multiple steps?
                # Let's create one step per invocation for simplicity or just one step with the first name
                flow_step = FlowStep(type="event", name=invocations[0])
                flow_step.triggers = triggers
                
            elif step.flowOperationStep():
                s = step.flowOperationStep()
                s_name = s.name().getText()
                flow_step = FlowStep(type="operation", name=s_name)
                if s.flowOperationTail():
                    tail = s.flowOperationTail()
                    if tail.flowDelegate():
                        flow_step.delegate = tail.flowDelegate().name().getText()
                    if tail.flowEmitsClause():
                         if tail.flowEmitsClause().flowEventList():
                             flow_step.emits = [n.getText() for n in tail.flowEmitsClause().flowEventList().name()]

            if flow_step:
                flow.steps.append(flow_step)

        if self.current_application:
            self.current_application.flows.append(flow)
        return flow

    def visitCoordination(self, ctx: CMLParser.CoordinationContext):
        name = ctx.name().getText()
        coord = Coordination(name=name)
        
        for step in ctx.coordinationStep():
            path = step.coordinationPath().getText()
            coord.steps.append(path)
            
        if self.current_application:
            self.current_application.coordinations.append(coord)
        return coord

    def visitModule(self, ctx: CMLParser.ModuleContext):
        name = ctx.name().getText()
        print(f"DEBUG: visitModule START {name}")
        module = Module(name=name)
        
        self.current_module = module
        if ctx.body:
            self.visit(ctx.body)
        self.current_module = None
        
        if self.current_context:
            self.current_context.modules.append(module)
        return module

    def visitCommandEvent(self, ctx: CMLParser.CommandEventContext):
        name = ctx.name(0).getText()
        ce = CommandEvent(name=name)
        
        if len(ctx.name()) > 1:
            ce.extends = ctx.name(1).getText()
            
        if ctx.body:
            self.current_domain_event = ce # Reuse domain event logic for attributes/ops
            for feature in ctx.body.feature():
                self.visit(feature)
            self.current_domain_event = None
            
        if self.current_aggregate:
            self.current_aggregate.command_events.append(ce)
        return ce

    def visitDataTransferObject(self, ctx: CMLParser.DataTransferObjectContext):
        name = ctx.name(0).getText()
        dto = DataTransferObject(name=name)
        
        if len(ctx.name()) > 1:
            dto.extends = ctx.name(1).getText()
            
        if ctx.body:
            # Reuse logic? DTOs have features too.
            # We can reuse current_value_object or current_entity logic if we set it temporarily
            # Or just duplicate the attribute logic.
            # Let's set it as current_value_object as it's similar
            self.current_value_object = dto
            for feature in ctx.body.feature():
                self.visit(feature)
            self.current_value_object = None
            
        if self.current_aggregate:
            self.current_aggregate.data_transfer_objects.append(dto)
        return dto
