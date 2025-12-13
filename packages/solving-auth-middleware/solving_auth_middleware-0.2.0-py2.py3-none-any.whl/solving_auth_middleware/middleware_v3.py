"""
Middleware d'authentification v3 - Version améliorée avec système de validators modulaires.

Cette version permet de définir des règles de validation d'accès de manière flexible
en combinant différents validators.
"""

from functools import wraps
from typing import List, Optional, Callable, Union
from flask import current_app, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask_jwt_extended.exceptions import (
    JWTExtendedException,
    JWTDecodeError,
    InvalidHeaderError,
    InvalidQueryParamError,
    NoAuthorizationError,
    CSRFError,
    WrongTokenError,
    RevokedTokenError,
    FreshTokenRequired,
    UserLookupError,
    UserClaimsVerificationError
)

from solving_auth_middleware.validators import AccessValidator
from solving_auth_middleware.enums import UserTypeEnum


def requires_access(
    validators: Union[AccessValidator, List[AccessValidator]],
    location: str = 'headers',
    fresh: bool = False,
    audit_fn: Optional[Callable] = None,
    on_success_fn: Optional[Callable] = None,
    include_resource: bool = False
):
    """
    Décorateur moderne pour la validation d'accès basée sur des validators modulaires.
    
    Args:
        validators: Un validator ou une liste de validators à appliquer
        location: Emplacement du token ('headers', 'cookies', 'query_string', 'json')
        fresh: Si True, exige un token frais
        audit_fn: Fonction optionnelle pour l'audit (identity, request, jwt_data)
        on_success_fn: Fonction appelée en cas de succès (jwt_data, identity, **kwargs)
        include_resource: Si True, passe les validators dans le contexte des kwargs
    
    Exemple:
        @requires_access(
            validators=[
                UserTypeValidator([UserTypeEnum.PRO, UserTypeEnum.SOFTWARE_ADMIN]),
                PermissionsValidator(['read', 'write'], mode='all')
            ],
            fresh=True
        )
        def my_route():
            return {"status": "ok"}
    """
    def wrapper(fn):
        @wraps(fn)
        @jwt_required(locations=[location], fresh=fresh)
        def decorator(*args, **kwargs):
            try:
                # Récupération des informations du JWT
                jwt_data = get_jwt()
                identity = get_jwt_identity()
                
                # Extraction du token selon la location
                token = _extract_token(location)
                
                # Log pour debugging
                current_app.logger.debug(f"Access validation - Identity: {identity}, User type: {jwt_data.get('user_type')}")
                
                # Normaliser validators en liste
                validators_list = validators if isinstance(validators, list) else [validators]
                
                # Préparation du contexte enrichi avec les données de la requête
                context = {
                    'kwargs': kwargs,
                    'args': args,
                    'request': request,
                    'request_json': request.get_json(silent=True) or {},
                    'request_form': request.form.to_dict() if request.form else {},
                    'request_args': request.args.to_dict() if request.args else {},
                }
                
                # Validation avec chaque validator
                for validator in validators_list:
                    is_valid, error_msg = validator.validate(jwt_data, identity, token, **context)
                    
                    if not is_valid:
                        current_app.logger.warning(
                            f"Access denied for {identity}: {error_msg}"
                        )
                        return {"msg": error_msg or "Accès refusé"}, 403
                
                # Audit si nécessaire
                if audit_fn:
                    try:
                        audit_fn(identity, request, jwt_data)
                    except Exception as e:
                        current_app.logger.error(f"Audit function error: {e}")
                
                # Callback de succès
                if on_success_fn:
                    try:
                        on_success_fn(jwt_data, identity, **kwargs)
                    except Exception as e:
                        current_app.logger.error(f"Success callback error: {e}")
                
                # Exécution de la fonction décorée
                return fn(*args, **kwargs)
                
            except NoAuthorizationError as e:
                return {"msg": "Token d'autorisation manquant", "error": str(e)}, 401
            except JWTDecodeError as e:
                return {"msg": "Format de token invalide", "error": str(e)}, 401
            except InvalidHeaderError as e:
                return {"msg": "En-tête d'autorisation invalide", "error": str(e)}, 401
            except InvalidQueryParamError as e:
                return {"msg": "Paramètre de requête invalide", "error": str(e)}, 401
            except CSRFError as e:
                return {"msg": "Protection CSRF échouée", "error": str(e)}, 401
            except WrongTokenError as e:
                return {"msg": "Type de token incorrect", "error": str(e)}, 401
            except RevokedTokenError as e:
                return {"msg": "Token révoqué", "error": str(e)}, 401
            except FreshTokenRequired as e:
                return {"msg": "Token frais requis", "error": str(e)}, 401
            except UserLookupError as e:
                return {"msg": "Utilisateur non trouvé", "error": str(e)}, 401
            except UserClaimsVerificationError as e:
                return {"msg": "Claims utilisateur invalides", "error": str(e)}, 401
            except JWTExtendedException as e:
                return {"msg": "Erreur JWT", "error": str(e)}, 401
            except Exception as e:
                current_app.logger.error(f"Unexpected error in access validation: {e}")
                return {"msg": "Erreur lors de la validation d'accès", "error": str(e)}, 500
        
        return decorator
    return wrapper


def _extract_token(location: str) -> str:
    """Extrait le token selon sa location."""
    if location == 'headers':
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
    elif location == 'cookies':
        return request.cookies.get('access_token_cookie', '')
    elif location == 'query_string':
        return request.args.get('jwt', '')
    elif location == 'json':
        return request.json.get('jwt', '') if request.json else ''
    
    return ''


# Alias pour compatibilité et clarté
requires_permissions_v3 = requires_access


# Helpers pour créer rapidement des validators courants
def quick_user_type_check(*user_types: UserTypeEnum):
    """
    Crée rapidement un validator pour vérifier le type d'utilisateur.
    
    Exemple:
        @requires_access(quick_user_type_check(UserTypeEnum.PRO, UserTypeEnum.SOFTWARE_ADMIN))
        def my_route():
            pass
    """
    from solving_auth_middleware.validators import UserTypeValidator
    return UserTypeValidator(list(user_types))


def quick_permissions_check(permissions: List[str], mode: str = "all"):
    """
    Crée rapidement un validator pour vérifier les permissions.
    
    Exemple:
        @requires_access(quick_permissions_check(['read', 'write']))
        def my_route():
            pass
    """
    from solving_auth_middleware.validators import PermissionsValidator
    return PermissionsValidator(permissions, mode)


def quick_role_hierarchy_check(minimum_role: UserTypeEnum):
    """
    Crée rapidement un validator pour vérifier la hiérarchie de rôles.
    
    Exemple:
        @requires_access(quick_role_hierarchy_check(UserTypeEnum.SOFTWARE_ADMIN))
        def my_route():
            pass
    """
    from solving_auth_middleware.validators import RoleHierarchyValidator
    return RoleHierarchyValidator(minimum_role)


def quick_resource_access_check(
    endpoint: str,
    resource_type: str,
    resource_id_mapping: dict,
    user_id_field: str = 'sub',
    additional_fields: Optional[dict] = None,
    timeout: int = 10,
    payload_format: str = 'standard'
):
    """
    Crée rapidement un validator pour vérifier l'accès à une ressource via un microservice.
    
    Cette fonction simplifie la création d'un ResourceAccessValidator pour les cas d'usage courants
    où vous devez vérifier qu'un utilisateur a accès à une ressource spécifique.
    
    Args:
        endpoint: URL du microservice de vérification d'accès
        resource_type: Type de ressource (ex: 'patient', 'family', 'document')
        resource_id_mapping: Mapping des IDs de ressources et leur source
            Format: {'field_name': 'source'}
            Sources possibles: 'url' (kwargs), 'json' (request body), 'form', 'query'
            Exemple: {'patient_id': 'url', 'family_id': 'json'}
        user_id_field: Nom du champ dans le JWT contenant l'ID utilisateur (défaut: 'sub')
        additional_fields: Champs supplémentaires à extraire (optionnel)
        timeout: Timeout en secondes pour l'appel API
        payload_format: Format du payload ('standard' ou 'flat')
    
    Exemple avec un patient (ID depuis l'URL):
        @requires_access([
            quick_user_type_check(UserTypeEnum.PRO),
            quick_resource_access_check(
                endpoint='http://api/check-patient-access',
                resource_type='patient',
                resource_id_mapping={'patient_id': 'url'},
                user_id_field='professional_id'
            )
        ])
        def get(self, patient_id):
            return {"patient": patient_id}
    
    Exemple avec une famille (ID depuis le JSON):
        @requires_access([
            quick_user_type_check(UserTypeEnum.PRO),
            quick_resource_access_check(
                endpoint='http://api/check-family-access',
                resource_type='family',
                resource_id_mapping={'family_id': 'json'},
                user_id_field='professional_id'
            )
        ])
        def post(self):
            # request.json contient {'family_id': '123', ...}
            return {"status": "ok"}
    
    Exemple avec plusieurs IDs (URL + JSON):
        @requires_access([
            quick_user_type_check(UserTypeEnum.PRO),
            quick_resource_access_check(
                endpoint='http://api/check-document-access',
                resource_type='document',
                resource_id_mapping={
                    'patient_id': 'url',
                    'document_id': 'json'
                },
                user_id_field='professional_id'
            )
        ])
        def post(self, patient_id):
            # patient_id depuis URL, document_id depuis request.json
            return {"status": "ok"}
    """
    from solving_auth_middleware.validators import ResourceAccessValidator
    return ResourceAccessValidator(
        endpoint=endpoint,
        resource_type=resource_type,
        resource_id_mapping=resource_id_mapping,
        user_id_field=user_id_field,
        additional_fields=additional_fields,
        timeout=timeout,
        payload_format=payload_format
    )

